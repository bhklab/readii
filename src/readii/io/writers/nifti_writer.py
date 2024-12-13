from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

import numpy as np
import SimpleITK as sitk

from readii.io.writers.base_writer import BaseWriter
from readii.utils import logger


class NiftiWriterError(Exception):
	"""Base exception for NiftiWriter errors."""

	pass


class NiftiWriterValidationError(NiftiWriterError):
	"""Raised when validation of writer configuration fails."""

	pass


class NiftiWriterIOError(NiftiWriterError):
	"""Raised when I/O operations fail."""

	pass


@dataclass
class NIFTIWriter(BaseWriter):
	"""Class for managing file writing with customizable paths and filenames for NIFTI files."""

	compression_level: int = field(
		default=9,
		metadata={
			"help": "Compression level (0-9). Higher values mean better compression but slower writing."
		},
	)
	overwrite: bool = field(
		default=False,
		metadata={
			"help": "If True, allows overwriting existing files. If False, raises FileExistsError."
		},
	)

	# Make extensions immutable
	VALID_EXTENSIONS: ClassVar[list[str]] = [
		".nii",
		".nii.gz",
	]
	MAX_COMPRESSION_LEVEL: ClassVar[int] = 9
	MIN_COMPRESSION_LEVEL: ClassVar[int] = 0

	def __post_init__(self) -> None:
		"""Validate writer configuration."""
		super().__post_init__()

		if not self.MIN_COMPRESSION_LEVEL <= self.compression_level <= self.MAX_COMPRESSION_LEVEL:
			msg = f"Invalid compression level {self.compression_level}. Must be between {self.MIN_COMPRESSION_LEVEL} and {self.MAX_COMPRESSION_LEVEL}."
			raise NiftiWriterValidationError(msg)

		if not any(self.filename_format.endswith(ext) for ext in self.VALID_EXTENSIONS):
			msg = f"Invalid filename format {self.filename_format}. Must end with one of {self.VALID_EXTENSIONS}."
			raise NiftiWriterValidationError(msg)

	def save(self, image: sitk.Image | np.ndarray, PatientID: str, **kwargs: str | int) -> Path:
		"""Write the SimpleITK image to a NIFTI file.

		Parameters
		----------
		image : sitk.Image | np.ndarray
			The SimpleITK image to save
		PatientID : str
			Required patient identifier
		**kwargs : str | int
			Additional formatting parameters for the output path

		Returns
		-------
		Path
			Path to the saved file

		Raises
		------
		NiftiWriterIOError
			If file exists and overwrite=False or if writing fails
		NiftiWriterValidationError
			If image is invalid
		"""
		match image:
			case sitk.Image():
				pass
			case np.ndarray():
				image = sitk.GetImageFromArray(image)
			case _:
				msg = "Input must be a SimpleITK Image or a numpy array"
				raise NiftiWriterValidationError(msg)

		logger.debug("Saving.", kwargs=kwargs)

		out_path = self.resolve_path(PatientID=PatientID, **kwargs)
		if out_path.exists():
			if not self.overwrite:
				msg = f"File {out_path} already exists. \nSet {self.__class__.__name__}.overwrite to True to overwrite."
				raise NiftiWriterIOError(msg)
			else:
				logger.warning(f"File {out_path} already exists. Overwriting.")

		logger.debug("Writing image to file", out_path=out_path)
		try:
			sitk.WriteImage(
				image, str(out_path), useCompression=True, compressionLevel=self.compression_level
			)
		except Exception as e:
			msg = f"Error writing image to file {out_path}: {e}"
			raise NiftiWriterIOError(msg) from e
		else:
			logger.info("Image saved successfully.", out_path=out_path)
			return out_path


if __name__ == "__main__": # pragma: no cover
	from rich import print  # noqa

	nifti_writer = NIFTIWriter(
		root_directory=Path("TRASH", "nifti_writer_examples"),
		filename_format="{NegativeControl}_{Region}/{SubjectID}_{Modality}.nii.gz",
		compression_level=9,
		overwrite=False,
		create_dirs=True,
	)

	print(nifti_writer)
