import numpy as np

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