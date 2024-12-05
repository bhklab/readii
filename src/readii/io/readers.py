import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import SimpleITK as sitk
from imgtools.dicom.sort.parser import PatternParser

from readii.utils import logger


@dataclass
class BaseReader:
	"""Abstract base class for reading and extracting metadata from files based on a filename pattern."""

	root_directory: Path
	filename_pattern: str
	pattern_parser: PatternParser = field(init=False)
	DEFAULT_PATTERN: re.Pattern = field(
		default=re.compile(r"%([A-Za-z]+)|\{([A-Za-z]+)\}"), init=False
	)

	def __post_init__(self) -> None:
		"""Initialize and validate the filename pattern parser."""
		# Ensure root_directory is a valid Path object
		self.root_directory = Path(self.root_directory)

		# Validate and initialize the pattern parser
		self._initialize_parser()

	def _initialize_parser(self) -> None:
		"""Initialize and validate the pattern parser."""
		self.pattern_parser = PatternParser(
			self.filename_pattern, pattern_parser=self.DEFAULT_PATTERN
		)
		try:
			self.pattern_parser.parse()  # Validate the pattern
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
		formatted_pattern, keys = self.pattern_parser.parse()

		# Construct a regex for matching the filename pattern
		regex_pattern = formatted_pattern.replace("%(", "(?P<").replace(")s", ">.*?)")
		matcher = re.match(regex_pattern, str(filepath))

		if not matcher:
			msg = f"Filename '{filepath}' does not match the expected pattern: {formatted_pattern}"
			logger.error(msg)
			raise ValueError(msg)

		return matcher.groupdict()

	def map_files(self) -> Dict[Path, Dict[str, Any]]:
		"""
		Map files in the root directory to their extracted metadata.

		Returns
		-------
		Dict[str, List[Path]]
			A dictionary mapping metadata keys to lists of file paths.
		"""
		mapping = defaultdict()

		for filepath in self.scan():
			try:
				metadata = self.extract_metadata(filepath.relative_to(self.root_directory))
				mapping[filepath] = metadata
			except ValueError:
				logger.warning(f"Skipping file {filepath}, as it does not match the pattern.")

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
	nifti_reader = NIFTIReader(
			root_directory=Path("TRASH/data/negative-controls-niftis"),
			filename_pattern="{SubjectID}/{Modality}/{NegativeControl}-{Region}.nii.gz",
	)

	results = nifti_reader.map_files()

	sampled = {k: v for k, v in results.items() if v["NegativeControl"] == "sampled"}

	print(sampled)
