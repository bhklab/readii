import numpy as np
from scipy.ndimage import binary_dilation

from .abstract_classes import RegionStrategy


class FullRegion(RegionStrategy):
	"""Region strategy to apply control to the entire image."""

	region_name = "full"

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""Apply the region mask to the image array."""
		# region_mask in this case is just everything
		region_mask = np.ones_like(mask_array)
		return region_mask


class ROIRegion(RegionStrategy):
	"""Region strategy to apply control within the ROI."""

	region_name = "roi"

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""Apply the region mask to the image array."""
		region_mask = np.where(mask_array > 0, 1, 0)
		if not region_mask.any():
			msg = "ROI mask is all 0s. No pixels in ROI to apply negative control."
			raise ValueError(msg)
		return region_mask


class NonROIRegion(RegionStrategy):
	"""Region strategy to apply control outside the ROI."""

	region_name = "non_roi"

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""Apply the region mask to the image array."""
		region_mask = np.where(mask_array > 0, 0, 1)
		if not region_mask.any():
			msg = "Non-ROI mask is all 0s. No pixels outside ROI to apply negative control."
			raise ValueError(msg)
		return region_mask


class NonROIWithBorderRegion(RegionStrategy):
	"""Region strategy to apply control outside the ROI, including a 2-pixel border."""

	region_name = "non_roi_with_border"
	# Add a 2-pixel border around the ROI
	padding = 1

	def __call__(self, image_array: np.ndarray, mask_array: np.ndarray) -> np.ndarray:
		"""
		Apply the region mask to the image array, adding a border of 2 pixels around the ROI.

		Parameters
		----------
		image_array : np.ndarray
			The base image as a numpy array.
		mask_array : np.ndarray
			The binary mask defining the ROI.

		Returns
		-------
		np.ndarray
			A binary mask with 1s outside the ROI and its 2-pixel border.
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
