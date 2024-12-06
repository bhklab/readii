import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

import SimpleITK as sitk
from imgtools.dicom.sort.parser import PatternParser

from readii.utils import logger


@dataclass
class BaseReader:
	"""Abstract base class for reading and extracting metadata from files based on a filename pattern.
	
	Main idea here is to extract metadata from a file path based on a pattern. 

	i.e given the following file path:
	/JohnDoe/CT/sampled-ROI.nii.gz
	and the following pattern:
	{SubjectID}/{Modality}/{NegativeControl}-{Region}.nii.gz

	The metadata would be:
	{"SubjectID": "JohnDoe", "Modality": "CT", "NegativeControl": "sampled", "Region": "ROI"}

	Parameters
	----------
	root_directory : Path
		The root directory to search for files.
	filename_pattern : str
		The pattern to use to extract metadata from file paths. Must be relative to the root_directory.
		This pattern should include placeholders for the metadata keys.
		Placeholders can be in the form of {key} or %(key)s.
	ignore_unmatched : bool, optional
		Whether to ignore files that do not match the pattern. Default is True.
		Otherwise, warnings will be logged for unmatched files.
	
	Attributes
	----------
	root_directory : Path
		The root directory to search for files.
	filename_pattern : str
		The pattern to use to extract metadata from file paths. Must be relative to the root_directory.
		This pattern should include placeholders for the metadata keys.
		Placeholders can be in the form of {key} or %(key)s.
	ignore_unmatched : bool, optional
		Whether to ignore files that do not match the pattern. Default is True.
		Otherwise, warnings will be logged for unmatched files.
	pattern_parser : PatternParser
		The pattern parser object used to extract metadata from file paths.
	mapping : List[Dict[str, Path | str]]
		A list of dictionaries containing the extracted metadata for each file.
		Returned by the `map_files` method.
	"""

	root_directory: Path
	filename_pattern: str
	ignore_unmatched: bool = True

	# pattern_parser is initialized in __post_init__ from the filename_pattern
	pattern_parser: PatternParser = field(init=False)
	DEFAULT_PATTERN: re.Pattern = field(
		default=re.compile(r"%([A-Za-z]+)|\{([A-Za-z]+)\}"), 
		init=False
	)
	formatted_pattern: str = field(init=False)
	keys: Set[str] = field(init=False)
	mapping: List = field(default_factory=list, init=False)

	def __post_init__(self) -> None:
		"""Initialize and validate the filename pattern parser."""
		# Ensure root_directory is a valid Path object
		self.root_directory = Path(self.root_directory)

		# Validate and initialize the pattern parser
		self._initialize_parser()

	def _initialize_parser(self) -> None:
		"""Initialize and validate the pattern parser."""
		self.pattern_parser = PatternParser(
			pattern=self.filename_pattern,
			pattern_parser=self.DEFAULT_PATTERN
		)
		try:
			self.formatted_pattern, self.keys = self.pattern_parser.parse()
		except Exception as e:
			msg = f"Invalid filename pattern: {e}"
			raise ValueError(msg) from e

	def scan(self) -> List[Path]:
		"""Scan the root directory for files matching the filename pattern."""
		return [f for f in self.root_directory.rglob("*") if f.is_file()]

	def extract_metadata(self, filepath: Path) -> Dict[str, Any]:
		"""
		Extract metadata from a filepath based on the filename pattern.

		Parameters
		----------
		filepath : Path
			Path to the file whose metadata needs to be extracted.

		Returns
		-------
		Dict[str, Any]
			Dictionary containing extracted metadata.

		Raises
		------
		ValueError
			If the filename does not match the pattern.
		"""
		# Construct a regex for matching the filename pattern
		regex_pattern = self.formatted_pattern.replace("%(", "(?P<").replace(")s", ">.*?)")
		matcher = re.match(regex_pattern, str(filepath))

		if matcher:
			return matcher.groupdict()
		msg = f"Filename '{filepath}' does not match the expected pattern: {self.formatted_pattern}"
		raise ValueError(msg)

	# def map_files(self) -> Dict[Path, Dict[str, Any]]:
	def map_files(self) -> List[Dict[str, Path | str]]:
		"""
		Map files in the root directory to their extracted metadata.

		Returns
		-------
		Dict[str, List[Path]]
			A dictionary mapping metadata keys to lists of file paths.
		"""
		mapping = []
		unmatched = []
		for filepath in self.scan():
			try:
				metadata = self.extract_metadata(filepath.relative_to(self.root_directory))
				metadata["filepath"] = filepath
				mapping.append(metadata)
			except ValueError as ve:
				unmatched.append(filepath)
				if self.ignore_unmatched:
					continue
				logger.warning(f"Skipping file {filepath}, as it does not match the pattern.", error=ve, valid_keys=self.keys)
		if unmatched:
			logger.debug(f"Unmatched files: {len(unmatched)}", unmatched=unmatched)
		return mapping

@dataclass
class NIFTIReader(BaseReader):
	"""Class for reading and mapping NIFTI files based on a filename pattern."""

	def load_image(self, filepath: Path) -> Optional[sitk.Image]:
		"""
		Load a NIFTI image from the given filepath.

		Parameters
		----------
		filepath : Path
			Path to the NIFTI file.

		Returns
		-------
		sitk.Image or None
			The loaded NIFTI image or None if loading fails.
		"""
		try:
			logger.debug("Loading NIFTI image", filepath=filepath)
			return sitk.ReadImage(str(filepath))
		except Exception as e:
			logger.error(f"Failed to load NIFTI file: {filepath}. Error: {e}")
			return None


if __name__ == "__main__":
	from pathlib import Path  # noqa
	from rich import print
	
	nifti_reader = NIFTIReader(
			root_directory=Path("TRASH/data/negative-controls-niftis"),
			filename_pattern="{SubjectID}/{Modality}/{NegativeControl}-{Region}.nii.gz",
	)

	results = nifti_reader.map_files()


	print(results)
