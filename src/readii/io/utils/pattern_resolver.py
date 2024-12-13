import re
from dataclasses import dataclass, field
from typing import Any, ClassVar, Dict, Tuple

from imgtools.dicom.sort.exceptions import InvalidPatternError  # type: ignore
from imgtools.dicom.sort.parser import PatternParser  # type: ignore

from readii.utils import logger


# Define custom exceptions
class PatternResolverError(Exception):
	"""Base exception for errors in pattern resolution."""

	pass

@dataclass
class PatternResolver:
	r"""Handles parsing and validating filename patterns.
	
	By default, this class uses the following pattern parser:

	>>> DEFAULT_PATTERN: re.Pattern = re.compile(r"%(\w+)|\{(\w+)\}")

	This will match placeholders of the form `{key}` or `%(key)s`.
	
	Example
	-------
	Given a filename format like `"{subject_id}_{date}/{disease}.txt"`, the pattern parser 
	will extract the following keys:

	>>> pattern_resolver.keys
	{'subject_id', 'date', 'disease'}

	And the following formatted pattern:

	>>> pattern_resolver.formatted_pattern
	%(subject_id)s_%(date)s/%(disease)s.txt

	So you could resolve the pattern like this:

	>>> data_dict = {"subject_id": "JohnDoe", "date": "January-01-2025", "disease": "cancer"}

	>>> pattern_resolver.formatted_pattern % data_dict 
	'JohnDoe_01-01-2025/cancer.txt'

	A more convenient way to resolve the pattern is to use the `resolve` method:	
	>>> pattern_resolver.resolve(data_dict))
	'JohnDoe_01-01-2025/cancer.txt'
	"""

	filename_format: str = field(init=True)

	DEFAULT_PATTERN: ClassVar[re.Pattern] = re.compile(r"%(\w+)|\{(\w+)\}")

	def __init__(self, filename_format: str) -> None:
		self.filename_format = filename_format

		try:
			self.pattern_parser = PatternParser(
				self.filename_format, pattern_parser=self.DEFAULT_PATTERN
			)
			self.formatted_pattern, self.keys = self.parse()  # Validate the pattern by parsing it
		except InvalidPatternError as e:
			msg = f"Invalid filename format: {e}"
			raise PatternResolverError(msg) from e
		else:
			logger.debug("All keys are valid.", keys=self.keys)
			logger.debug("Formatted Pattern valid.", formatted_pattern=self.formatted_pattern)

	def parse(self) -> Tuple[str, list[str]]:
		"""
		Parse and validate the pattern.

		Returns
		-------
		Tuple[str, List[str]]
			The formatted pattern string and a list of extracted keys.

		Raises
		------
		InvalidPatternError
			If the pattern contains no valid placeholders or is invalid.
		"""
		formatted_pattern, keys = self.pattern_parser.parse()
		return formatted_pattern, keys

	def resolve(self, context: Dict[str, Any]) -> str:
		"""Resolve the pattern using the provided context dictionary.

		Parameters
		----------
		context : Dict[str, Any]
			Dictionary containing key-value pairs to substitute in the pattern.

		Returns
		-------
		str
			The resolved pattern string with placeholders replaced by values.

		Raises
		------
		PatternResolverError
			If a required key is missing from the context dictionary.
		"""
		if None in context.values():
			msg = "None is not a valid value for a placeholder in the pattern."
			none_keys = [key for key, value in context.items() if value is None]
			msg += f" None keys: {none_keys}"
			raise PatternResolverError(msg)

		try:
			return self.formatted_pattern % context
		except KeyError as e:
			# missing_key = e.args[0]
			missing_keys = set(context.keys()) - set(self.keys)
			msg = f"Missing value for placeholder(s): {missing_keys}"
			msg += "\nPlease provide a value for this key in the `context` argument."
			msg += f" i.e `{self.__class__.__name__}.save(..., {e.args[0]}=value)`."
			raise PatternResolverError(msg) from e