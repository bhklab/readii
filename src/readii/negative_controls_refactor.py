from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from itertools import product
from typing import Dict, Iterator, List, Optional, Type, TypeVar

import numpy as np
import SimpleITK as sitk

from readii.utils import logger

logger.setLevel("DEBUG")

# Define a TypeVar for the input types
T = TypeVar("T", sitk.Image, np.ndarray)


#################################################################
# ABSTRACT CLASSES
#################################################################

class RegionStrategy(ABC):
	"""Abstract class for defining how to apply a region mask."""

	@abstractmethod
	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""
		Apply the region mask to the image array.
		"""
		pass

	@classmethod
	def name(cls) -> str:
		return cls.region_name

@dataclass
class NegativeControlStrategy(ABC):
	"""Abstract class for negative control strategies.

	This class defines the interface for negative control strategies.
	Subclasses should implement the abstract methods to provide the specific implementation for the
	negative control strategy.
	"""

	random_seed: Optional[int] = field(default=None, metadata={"description": "Seed for reproducibility"})

	@abstractmethod
	def transform(self, image_array: np.ndarray) -> np.ndarray:
		"""Abstract method for applying the specific transformation.

		Subclasses should implement this method to apply the specific transformation.

		Note: The returned array should have the same dimension and size as the input array.
		"""
		pass

	@classmethod
	def name(cls) -> str:
		return cls.negative_control_name

	def __call__(
		self, 
		image: T,
		mask: Optional[T] = None,
		region: Optional[RegionStrategy] = None,	
	) -> T:
		"""
		Apply the negative control strategy to the input image.

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
	def to_array(input_data: T) -> np.ndarray:
		"""Convert SimpleITK Image to numpy array if needed."""
		match input_data:
			case sitk.Image():
				return sitk.GetArrayFromImage(input_data)
			case np.ndarray():
				return input_data
			case _:
				msg = f"input_data must be SimpleITK Image or numpy array, got {type(input_data)}"
				raise TypeError(msg)

#################################################################
# REGION STRATEGIES
#################################################################

class FullRegion(RegionStrategy):

	region_name = "full"

	"""Region strategy to apply control to the entire image."""
	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		# region_mask in this case is just everything
		region_mask = np.ones_like(mask_array)
		return region_mask

class ROIRegion(RegionStrategy):

	region_name = "roi"

	"""Region strategy to apply control within the ROI."""

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		region_mask = np.where(mask_array > 0, 1, 0)
		if not region_mask.any():
			msg = "ROI mask is all 0s. No pixels in ROI to apply negative control."
			raise ValueError(msg)
		return region_mask

class NonROIRegion(RegionStrategy):

	region_name = "non_roi"

	"""Region strategy to apply control outside the ROI."""

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		region_mask = np.where(mask_array > 0, 0, 1)
		if not region_mask.any():
			msg = "Non-ROI mask is all 0s. No pixels outside ROI to apply negative control."
			raise ValueError(msg)
		return region_mask


#################################################################
# NEGATIVE CONTROL STRATEGIES
#################################################################

class ShuffledControl(NegativeControlStrategy):
	"""Shuffle pixel values within the image."""

	negative_control_name = "shuffled"

	def transform(self, image_array: np.ndarray) -> np.ndarray:
		"""Shuffle pixel values."""
		# Get array dimensions to reshape back to
		img_dimensions = image_array.shape

		# Flatten the 3D array to 1D so values can be shuffled
		flat_array_image = image_array.flatten()

		# Set the random seed for np random generator
		rng = np.random.default_rng(seed=self.random_seed)

		# Shuffle the flat array
		rng.shuffle(flat_array_image)

		# Reshape the array back into the original image dimensions
		shuffled_image = np.reshape(flat_array_image, img_dimensions)

		return shuffled_image

class SampledControl(NegativeControlStrategy):

	negative_control_name = "sampled"

	"""Randomly sample pixel values from the distribution of existing pixel values within the image."""

	def transform(self, image_array: np.ndarray) -> np.ndarray:
		# Get array dimensions to reshape back to
		imgDimensions = image_array.shape

		# Flatten the 3D array to 1D so values can be shuffled
		flatArrImage = image_array.flatten()

		# Set the random seed for np random number generator
		randNumGen = np.random.default_rng(seed=self.random_seed)

		# Randomly sample values for new array from original image distribution
		sampled_array = randNumGen.choice(flatArrImage, size=len(flatArrImage), replace=True)

		# Reshape the array back into the original image dimensions
		randomlySampled3DArrImage = np.reshape(sampled_array, imgDimensions)

		return randomlySampled3DArrImage

class RandomizedControl(NegativeControlStrategy):
	"""Randomly generate pixel values within the image."""

	negative_control_name = "randomized"

	def transform(self, image_array: np.ndarray) -> np.ndarray:
		# Get array dimensions to reshape back to
		imgDimensions = image_array.shape

		# Get min and max HU values to set as range for random values
		minVoxelVal = np.min(image_array)
		maxVoxelVal = np.max(image_array)

		# Set the random seed for np random generator
		randNumGen = np.random.default_rng(seed=self.random_seed)

		# Generate random array with same dimensions as baseImage with values ranging from the minimum to maximum inclusive of the original image
		random3DArr = randNumGen.integers(
			low=minVoxelVal, high=maxVoxelVal, endpoint=True, size=imgDimensions, dtype=np.uint8
		)
		return random3DArr


#################################################################
# CLASS REGISTRIES
#################################################################

# Using the `strategy_name` attributes directly
REGION_REGISTRY: Dict[str, Type[RegionStrategy]] = {
    cls.name(): cls
    for cls in [FullRegion, ROIRegion, NonROIRegion]
}

NEGATIVE_CONTROL_REGISTRY: Dict[str, Type[NegativeControlStrategy]] = {
    cls.name(): cls
    for cls in [ShuffledControl, SampledControl, RandomizedControl]
}


@dataclass
class NegativeControlManager:
    """
    Manager class for applying negative control strategies to images.
    """
    negative_control_strategies: List[NegativeControlStrategy]
    region_strategies: List[RegionStrategy]

    @classmethod
    def from_strings(
        cls,
        negative_control_types: List[str],
        region_types: List[str],
        random_seed: Optional[int] = None,
    ) -> "NegativeControlManager":
        """
        Create a NegativeControlManager instance from string representations.
        """
        negative_control_strategies = [
            NEGATIVE_CONTROL_REGISTRY[control_type](random_seed=random_seed)
            for control_type in negative_control_types
        ]

        region_strategies = [
            REGION_REGISTRY[region_type]()
            for region_type in region_types
        ]

        return cls(
            negative_control_strategies=negative_control_strategies,
            region_strategies=region_strategies,
        )

    def apply(self, base_image: T, mask: T) -> Iterator[tuple[T, str, str]]:
        """Apply the negative control strategies to the region strategies."""
        for control_strategy, region_strategy in product(
            self.negative_control_strategies, self.region_strategies
        ):
            yield (
                control_strategy(base_image, mask, region_strategy),
                control_strategy.name(),
                region_strategy.name(),
            )