from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, TypeVar

import numpy as np
import SimpleITK as sitk

# Define a TypeVar for image-like inputs
ImageInput = TypeVar("ImageInput", sitk.Image, np.ndarray)


@dataclass
class RegionStrategy(ABC):
	"""Abstract base class for defining how to apply a region mask."""

	# Add this class attribute to define the region name contract for subclasses
	region_name: str = field(init=False)

	@abstractmethod
	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""
		Abstract method to apply the region mask to the image array.

		Parameters
		----------
		image_array : np.ndarray
			The base image as a numpy array.
		mask_array : np.ndarray
			The mask defining the region to modify.

		Returns
		-------
		np.ndarray
			The modified region mask as a numpy array.

		Note
		----
		Not all concrete subclasses will need to use both image_array and mask_array.
		For example, the ROIRegion class only uses mask_array, without regard to image_array.
		"""
		pass

	@classmethod
	def name(cls) -> str:
		"""Get the name of the region strategy.

		Returns
		-------
			str: The name of the region strategy.
		"""
		return cls.region_name


@dataclass
class NegativeControlStrategy(ABC):
	"""Abstract class for negative control strategies.

	This class defines the interface for negative control strategies.
	Subclasses should implement the abstract methods to provide the specific implementation
	for the negative control strategy.
	"""

	# Add this class attribute to define the negative control name contract for subclasses
	negative_control_name: str = field(init=False)

	@abstractmethod
	def transform(self, image_array: np.ndarray) -> np.ndarray:
		"""Abstract method for applying the specific transformation.

		Subclasses should implement this method to apply the specific transformation.

		Note
		----
		The returned array should have the same dimension and size as the input array.
		"""
		pass

	@classmethod
	def name(cls) -> str:
		"""Return the name of the negative control strategy.

		Returns
		-------
		str
			The name defined in the class.
		"""
		return cls.negative_control_name

	def __call__(
		self,
		image: ImageInput,
		mask: Optional[ImageInput] = None,
		region: Optional[RegionStrategy] = None,
	) -> ImageInput:
		"""Apply the negative control strategy to the input image.

		Parameters
		----------
		image : sitk.Image | np.ndarray
			The input image.
		mask : sitk.Image | np.ndarray, optional
			The mask defining the region to apply the control.
		region : RegionStrategy, optional
			The strategy to handle the region logic.

		Returns
		-------
		sitk.Image | np.ndarray
			The transformed image.
		"""
		image_array = self.to_array(image)

		if mask is not None and region is not None:
			mask_array = self.to_array(mask)
			region_mask = region(image_array, mask_array)
			mask_indices = np.nonzero(region_mask)

			# Apply the control only within the specified region
			flat_region_values = image_array[mask_indices]
			transformed_values = self.transform(flat_region_values)
			image_array[mask_indices] = transformed_values
		else:
			# Apply the control to the entire image
			image_array = self.transform(image_array)

		if isinstance(image, sitk.Image):
			transformed_image = sitk.GetImageFromArray(image_array)
			transformed_image.CopyInformation(image)
			return transformed_image

		return image_array

	@staticmethod
	def to_array(input_data: ImageInput) -> np.ndarray:
		"""Convert SimpleITK Image to numpy array if needed."""
		match input_data:
			case sitk.Image():
				return sitk.GetArrayFromImage(input_data)
			case np.ndarray():
				return input_data
			case _:
				msg = f"input_data must be SimpleITK Image or numpy array, got {type(input_data)}"
				raise TypeError(msg)
