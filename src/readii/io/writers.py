import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import SimpleITK as sitk
from imgtools.dicom.sort.exceptions import InvalidPatternError
from imgtools.dicom.sort.parser import PatternParser

from readii.utils import logger


@dataclass
class BaseWriter(ABC):
	"""Abstract base class for managing file writing with customizable paths and filenames."""

	root_directory: Path
	filename_format: str
	create_dirs: bool = True
	pattern_parser: PatternParser = field(init=False)
	DEFAULT_PATTERN: re.Pattern = field(
		default=re.compile(r"%([A-Za-z]+)|\{([A-Za-z]+)\}"), init=False
	)

	def __post_init__(self) -> None:
		"""Perform post-initialization tasks, such as validating the filename format."""
		# Convert root_directory to Path and ensure it exists
		self.root_directory = Path(self.root_directory)
		if self.create_dirs:
			self.root_directory.mkdir(parents=True, exist_ok=True)

		# Initialize and validate the filename format using PatternParser
		self._initialize_parser()

	@abstractmethod
	def save(self, *args: Any, **kwargs: Any) -> Path:  # noqa
		"""Abstract method for writing data. Must be implemented by subclasses.

		Use the `resolve_path` method to generate a file path based on the filename format and additional parameters.
		"""
		pass

	def _initialize_parser(self) -> None:
		"""Initialize and validate the pattern parser."""
		try:
			# Use a default regex pattern for placeholders like `{Key}` if none is provided
			self.pattern_parser = PatternParser(
				self.filename_format, pattern_parser=self.DEFAULT_PATTERN
			)
			self.pattern_parser.parse()  # Validate the pattern by parsing it
		except InvalidPatternError as e:
			msg = f"Invalid filename format: {e}"
			raise ValueError(msg) from e

	def _generate_datetime_strings(self) -> dict[str, str]:
		"""
		Generate current date and time strings in various formats.

		Returns
		-------
		dict
				A dictionary containing 'date', 'time', and 'date_time' strings.
		"""
		now = datetime.now(timezone.utc)
		return {
			"date": now.strftime("%Y-%m-%d"),
			"time": now.strftime("%H%M%S"),
			"date_time": now.strftime("%Y-%m-%d_%H%M%S"),
		}

	def resolve_path(self, SubjectID: str, **kwargs: str) -> Path:
		"""
		Generate a file path based on the filename format, subject ID, and additional parameters.

		Parameters
		----------
		SubjectID : str
				A unique identifier for the subject.
		kwargs : dict
				Additional parameters for formatting the filename.

		Returns
		-------
		Path
				The full file path including the root directory and formatted filename.
		"""
		# Generate datetime strings
		date_time_values = self._generate_datetime_strings()

		# Merge datetime strings, SubjectID, and additional keys for formatting
		context = {**date_time_values, "SubjectID": SubjectID, **kwargs}

		# Parse and format the filename
		formatted_pattern, keys = self.pattern_parser.parse()
		logger.debug(
			"All keys are valid.", formatted_pattern=formatted_pattern, keys=keys, context=context
		)
		try:
			out_filename = formatted_pattern % context
		except KeyError as e:
			missing_key = e.args[0]
			msg = f"Missing value for placeholder '{missing_key}' in filename format `{formatted_pattern}`."

			contextkeys = ", ".join(context.keys())
			msg += f" context keys are: {contextkeys}"

			msg += "\nPlease provide a value for this key in the `kwargs` argument,"
			msg += f" i.e `writer.put(..., {missing_key}=value)`."
			logger.exception(msg)
			raise ValueError(msg) from e

		# Build the full file path
		out_path = self.root_directory / out_filename

		# Ensure the parent directory exists
		if self.create_dirs:
			out_path.parent.mkdir(parents=True, exist_ok=True)

		return out_path


class NIFTIWriter(BaseWriter):
	"""Class for managing file writing with customizable paths and filenames for NIFTI files."""

	def save(self, SubjectID: str, image: sitk.Image, **kwargs: str | int) -> Path:
		"""Write the given data to the file resolved by the given kwargs."""
		out_path = self.resolve_path(SubjectID, **kwargs)
		logger.debug("Writing image to file", out_path=out_path)
		sitk.WriteImage(image, str(out_path), useCompression=True, compressionLevel=5)
		return out_path


if __name__ == "__main__":  # noqa
	from pathlib import Path  # noqa

	# Example usage
	nifti_writer = NIFTIWriter(
		root_directory=Path("TRASH", "negative_controls"),
		filename_format="{NegativeControl}_{Region}/{date}-{SubjectID}_{Modality}.nii.gz",
	)

	# This would create a directory structure like:
	# TRASH/
	# 	negative_controls/
	#   	Randomized_ROI/
	#     	2022-01-01-JohnAdams_CT.nii.gz
	#   	Sampled_NonROI/
	#     	2022-01-01-JohnAdams_CT.nii.gz
	# note: this file structure is probably confusing, but just showing how the file names are generated

	# The keyword arguments passed here MUST match the placeholders in the filename format
	nifti_writer.save(
		SubjectID="JohnAdams",
		image=sitk.Image(10, 10, 10, sitk.sitkInt16),
		NegativeControl="Randomized",
		Region="Brain",
		Modality="CT",
		# note, the date and time are generated automatically!
	)
