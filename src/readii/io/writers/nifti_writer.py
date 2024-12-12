from dataclasses import dataclass, field
from pathlib import Path

import SimpleITK as sitk

from readii.io.writers.base_writer import BaseWriter
from readii.utils import logger


@dataclass
class NIFTIWriter(BaseWriter):
	"""Class for managing file writing with customizable paths and filenames for NIFTI files."""

	# The default compression level for NIFTI files
	# compression_level: int = 9
	# overwrite: bool = True
	compression_level: int = field(default=9)
	overwrite: bool = field(default=False)

	# You can enforce some required keys by explicitly defining them in the
	# signnature of the save method. I.e force including the PatientID key
	def save(self, image: sitk.Image, PatientID: str, **kwargs: str | int) -> Path:
		"""Write the given data to the file resolved by the given kwargs."""
		# iterate over all the class attributes and log themn
		logger.debug("Saving.", kwargs=kwargs)

		out_path = self.resolve_path(PatientID=PatientID, **kwargs)
		if out_path.exists():
			if not self.overwrite:
				msg = f"File {out_path} already exists. \nSet {self.__class__.__name__}.overwrite to True to overwrite."
				raise FileExistsError(msg)
			else:
				logger.warning(f"File {out_path} already exists. Overwriting.")

		logger.debug("Writing image to file", out_path=out_path)
		sitk.WriteImage(image, str(out_path), useCompression=True, compressionLevel=9)
		return out_path


@dataclass
class NRRDWriter(BaseWriter):
	"""Class for managing file writing with customizable paths and filenames for NRRD files."""

	# The default compression level for NRRD files
	compression_level: int = 9
	overwrite: bool = True

	def save(self, image: sitk.Image, PatientID: str, **kwargs: str | int) -> Path:
		"""Write the given data to the file resolved by the given kwargs."""
		# iterate over all the class attributes and log themn
		logger.debug("Saving.", kwargs=kwargs)
