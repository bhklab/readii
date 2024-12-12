import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType
from typing import Any, ClassVar, Dict, Optional, Tuple

from imgtools.dicom.sort.exceptions import InvalidPatternError
from imgtools.dicom.sort.parser import PatternParser

from readii.utils import logger


@dataclass
class PatternResolver:
	"""Handles parsing and validating filename patterns."""

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
			raise ValueError(msg) from e
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
		return self.pattern_parser.parse()

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
		ValueError
			If a required key is missing from the context dictionary.
		"""
		try:
			return self.formatted_pattern % context
		except KeyError as e:
			missing_key = e.args[0]
			valid_keys = ", ".join(context.keys())
			msg = f"Missing value for placeholder '{missing_key}'. Valid keys: {valid_keys}"
			msg += "\nPlease provide a value for this key in the `kwargs` argument,"
			msg += f" i.e `{self.__class__.__name__}.save(..., {missing_key}=value)`."
			raise ValueError(msg) from e


@dataclass
class BaseWriter(ABC):
	"""Abstract base class for managing file writing with customizable paths and filenames."""

	# Any subclass has to be initialized with a root directory and a filename format
	root_directory: Path
	filename_format: str

	# optionally, you can set create_dirs to False if you want to handle the directory creation yourself
	create_dirs: bool = field(default=True)

	# class-level pattern resolver instance shared across all instances
	pattern_resolver: ClassVar[PatternResolver] = field(init=False)

	def __post_init__(self) -> None:
		"""Initialize the writer with the given root directory and filename format."""
		self.root_directory = Path(self.root_directory)
		if self.create_dirs:
			self.root_directory.mkdir(parents=True, exist_ok=True)
		elif not self.root_directory.exists():
			msg = f"Root directory {self.root_directory} does not exist."
			raise FileNotFoundError(msg)
		self.pattern_resolver = PatternResolver(self.filename_format)

	@abstractmethod
	def save(self, *args: Any, **kwargs: Any) -> Path:  # noqa
		"""Abstract method for writing data. Must be implemented by subclasses."""
		pass

	def _generate_datetime_strings(self) -> dict[str, str]:
		now = datetime.now(timezone.utc)
		return {
			"date": now.strftime("%Y-%m-%d"),
			"time": now.strftime("%H%M%S"),
			"date_time": now.strftime("%Y-%m-%d_%H%M%S"),
		}

	def resolve_path(self, **kwargs: Any) -> Path:  # noqa
		"""Generate a file path based on the filename format, subject ID, and additional parameters."""
		context = {**self._generate_datetime_strings(), **kwargs}
		filename = self.pattern_resolver.resolve(context)
		out_path = self.root_directory / filename
		if self.create_dirs:
			out_path.parent.mkdir(parents=True, exist_ok=True)
		return out_path

	# Context Manager Implementation
	def __enter__(self) -> "BaseWriter":
		"""
		Enter the runtime context related to this writer.

		Useful if the writer needs to perform setup actions, such as
		opening connections or preparing resources.
		"""
		logger.debug(f"Entering context manager for {self.__class__.__name__}")
		return self

	def __exit__(
		self: "BaseWriter",
		exc_type: Optional[type],
		exc_value: Optional[BaseException],
		traceback: Optional[TracebackType],
	) -> None:
		"""
		Exit the runtime context related to this writer.

		Parameters
		----------
		exc_type : Optional[type]
				The exception type, if an exception was raised, otherwise None.
		exc_value : Optional[BaseException]
				The exception instance, if an exception was raised, otherwise None.
		traceback : Optional[Any]
				The traceback object, if an exception was raised, otherwise None.
		"""
		if exc_type:
			logger.error(
				f"Exception raised in {self.__class__.__name__} while in context manager: {exc_value}"
			)
		logger.debug(f"Exiting context manager for {self.__class__.__name__}")

		# if the root directory is empty, aka we created it but didn't write anything, delete it
		if (
			self.create_dirs
			and self.root_directory.exists()
			and not (self.root_directory.iterdir())
		):
			logger.debug(f"Deleting empty directory {self.root_directory}")
