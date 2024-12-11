from dataclasses import dataclass, field
from itertools import product
from typing import Iterator, List, Optional, TypeVar

import numpy as np
import SimpleITK as sitk

from .abstract_classes import NegativeControlStrategy, RegionStrategy
from .negative_controls import RandomizedControl, SampledControl, ShuffledControl
from .regions import FullRegion, NonROIRegion, ROIRegion

# Define a TypeVar for image-like inputs
ImageInput = TypeVar("ImageInput", sitk.Image, np.ndarray)


REGION_REGISTRY = {cls.region_name: cls for cls in [FullRegion, ROIRegion, NonROIRegion]}

NEGATIVE_CONTROL_REGISTRY = {
	cls.negative_control_name: cls for cls in [ShuffledControl, SampledControl, RandomizedControl]
}


@dataclass
class NegativeControlManager:
	"""Manager class for applying negative control strategies to images."""

	negative_control_strategies: List[NegativeControlStrategy] = field(default_factory=list)
	region_strategies: List[RegionStrategy] = field(default_factory=list)

	@classmethod
	def from_strings(
		cls,
		negative_control_types: List[str],
		region_types: List[str],
		random_seed: Optional[int] = None,
	) -> "NegativeControlManager":
		"""Create a NegativeControlManager instance from string representations."""
		negative_control_strategies = [
			NEGATIVE_CONTROL_REGISTRY[control_type](random_seed=random_seed)
			for control_type in negative_control_types
		]

		region_strategies = [REGION_REGISTRY[region_type]() for region_type in region_types]

		return cls(
			negative_control_strategies=negative_control_strategies,
			region_strategies=region_strategies,
		)

	@property
	def strategy_products(self) -> Iterator[tuple[NegativeControlStrategy, RegionStrategy]]:
		"""Get all combinations of negative control and region strategies."""
		return product(self.negative_control_strategies, self.region_strategies)

	def apply(
		self, base_image: ImageInput, mask: ImageInput
	) -> Iterator[tuple[ImageInput, str, str]]:
		"""Apply the negative control strategies to the region strategies."""
		for control_strategy, region_strategy in self.strategy_products:
			yield (
				control_strategy(base_image, mask, region_strategy),
				control_strategy.name(),
				region_strategy.name(),
			)

	def apply_single(
		self,
		base_image: ImageInput,
		mask: ImageInput,
		control_strategy: NegativeControlStrategy | str,
		region_strategy: RegionStrategy | str,
		random_seed: Optional[int] = None,
	) -> tuple[ImageInput, str, str]:
		"""Apply a single negative control strategy to a single region strategy.

		Parameters
		----------
		base_image : np.ndarray | sitk.Image
			The base image to apply the negative control to.
		mask : np.ndarray | sitk.Image
			The mask image defining regions of interest.
		control_strategy : NegativeControlStrategy or str
			The negative control strategy to apply. Can be either a NegativeControlStrategy
			instance or a string name from NEGATIVE_CONTROL_REGISTRY.
		region_strategy : RegionStrategy or str
			The region strategy to use. Can be either a RegionStrategy instance or a
			string name from REGION_REGISTRY.
		random_seed : int | None, optional
			Seed for random number generation, by default None.

		Returns
		-------
		tuple[ImageInput, str, str]
			A tuple containing:
			- The transformed image
			- The name of the control strategy used
			- The name of the region strategy used

		Raises
		------
		KeyError
			If a string strategy name is not found in the respective registry.
		"""
		if isinstance(control_strategy, str):
			control_strategy = NEGATIVE_CONTROL_REGISTRY[control_strategy]()
		if isinstance(region_strategy, str):
			region_strategy = REGION_REGISTRY[region_strategy]()

		if random_seed is not None:
			control_strategy.random_seed = random_seed

		return (
			control_strategy(base_image, mask, region_strategy),
			control_strategy.name(),
			region_strategy.name(),
		)

	def __len__(self) -> int:
		"""Return the total number of strategy combinations."""
		return len(list(self.strategy_products))

	def __repr__(self) -> str:
		"""Return a string representation of the manager."""
		return f"NegativeControlManager(negative_controls={len(self.negative_control_strategies)}, regions={len(self.region_strategies)})"
