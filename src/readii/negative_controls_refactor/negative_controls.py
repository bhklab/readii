from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from .abstract_classes import NegativeControlStrategy


@dataclass
class ShuffledControl(NegativeControlStrategy):
	"""Shuffle pixel values within the image."""

	negative_control_name = "shuffled"

	random_seed: Optional[int] = field(
		default=None, metadata={"description": "Seed for reproducibility"}
	)

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


@dataclass
class SampledControl(NegativeControlStrategy):
	"""Randomly sample pixel values with replacement from the distribution of existing pixel values within the image."""

	negative_control_name = "sampled"

	random_seed: Optional[int] = field(
		default=None, metadata={"description": "Seed for reproducibility"}
	)

	def transform(self, image_array: np.ndarray) -> np.ndarray:
		"""Randomly sample pixel values."""
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


@dataclass
class RandomizedControl(NegativeControlStrategy):
	"""Randomly generate pixel values within the range of the original image pixel values."""

	negative_control_name = "randomized"

	random_seed: Optional[int] = field(
		default=None, metadata={"description": "Seed for reproducibility"}
	)

	def transform(self, image_array: np.ndarray) -> np.ndarray:
		"""Randomly generate pixel values."""
		# Get array dimensions to reshape back to
		imgDimensions = image_array.shape

		# Get min and max HU values to set as range for random values
		minVoxelVal = np.min(image_array)
		maxVoxelVal = np.max(image_array)

		# Set the random seed for np random generator
		randNumGen = np.random.default_rng(seed=self.random_seed)

		# Generate random array with same dimensions as baseImage with values ranging from the minimum to maximum inclusive of the original image
		random3DArr = randNumGen.integers(
			low=minVoxelVal, high=maxVoxelVal, endpoint=True, size=imgDimensions
		)
		return random3DArr
