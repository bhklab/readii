from typing import Final

import numpy as np
from scipy.ndimage import binary_dilation

from .abstract_classes import RegionStrategy


class FullRegion(RegionStrategy):
	"""Region strategy to apply control to the entire image.

	A strategy that creates a mask covering the entire image array with ones,
	effectively selecting all pixels for processing.
	"""

	region_name: Final[str] = "full"

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""Apply the region mask to the image array.

		Parameters
		----------
		image_array : np.ndarray
		  The input image array (unused in this strategy)
		mask_array : np.ndarray
		  The input mask array (unused in this strategy)

		Returns
		-------
		np.ndarray
		  A binary mask of ones with the same shape as the input arrays
		"""
		region_mask = np.ones_like(mask_array)
		return region_mask


class ROIRegion(RegionStrategy):
	"""Region strategy to apply control within the ROI.

	A strategy that creates a mask matching the input ROI mask,
	selecting only pixels within the region of interest.
	"""

	region_name: Final[str] = "roi"

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""Apply the region mask to the image array.

		Parameters
		----------
		image_array : np.ndarray
		  The input image array (unused in this strategy)
		mask_array : np.ndarray
		  The binary mask defining the ROI

		Returns
		-------
		np.ndarray
		  A binary mask matching the ROI

		Raises
		------
		ValueError
		  If the resulting mask contains no positive pixels
		"""
		region_mask = np.where(mask_array > 0, 1, 0)
		if not region_mask.any():
			msg = "ROI mask is all 0s. No pixels in ROI to apply negative control."
			raise ValueError(msg)
		return region_mask


class NonROIRegion(RegionStrategy):
	"""Region strategy to apply control outside the ROI.

	A strategy that creates a mask selecting all pixels outside
	the region of interest.
	"""

	region_name: Final[str] = "non_roi"

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""Apply the region mask to the image array.

		Parameters
		----------
		image_array : np.ndarray
		  The input image array (unused in this strategy)
		mask_array : np.ndarray
		  The binary mask defining the ROI

		Returns
		-------
		np.ndarray
		  A binary mask with 1s outside the ROI

		Raises
		------
		ValueError
		  If the resulting mask contains no positive pixels
		"""
		region_mask = np.where(mask_array > 0, 0, 1)
		if not region_mask.any():
			msg = "Non-ROI mask is all 0s. No pixels outside ROI to apply negative control."
			raise ValueError(msg)
		return region_mask


class NonROIWithBorderRegion(RegionStrategy):
	"""Region strategy to apply control outside the ROI, including a configurable border.

	Parameters
	----------
	dilation_iterations : int, optional
		Number of iterations for binary dilation, by default 1.
		See https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.binary_dilation.html#binary-dilation
	"""

	region_name: Final[str] = "non_roi_with_border"

	def __init__(self, dilation_iterations: int = 1) -> None:
		"""Initialize the strategy with configurable padding.

		Parameters
		----------
		dilation_iterations : int, optional

		"""
		self.dilation_iterations = dilation_iterations

	def __call__(self, _: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""Apply the region mask to the image array, adding a border around the ROI.

		Parameters
		----------
		_ : np.ndarray
				The base image as a numpy array.
		mask_array : np.ndarray
				The binary mask defining the ROI.

		Returns
		-------
		np.ndarray
				A binary mask with 1s outside the ROI and its border.
		"""
		# Ensure mask_array is binary (0s and 1s)
		binary_mask = (mask_array > 0).astype(np.uint8)

		roi_with_border = binary_dilation(binary_mask, iterations=self.padding)

		# Create the inverse mask for everything outside the ROI and its border
		region_mask = np.where(roi_with_border > 0, 0, 1)

		# Validate that there are non-zero pixels in the resulting mask
		if not region_mask.any():
			msg = "ROI with border mask is all 0s. No pixels outside ROI and its border to apply control."
			raise ValueError(msg)

		return region_mask
