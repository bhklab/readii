from dataclasses import dataclass, field
from itertools import product
from typing import Iterator, List, Optional, TypeVar

import numpy as np
import SimpleITK as sitk

from .abstract_classes import PermutationStrategy, RegionStrategy
from .permutations import RandomPermutation, SamplePermutation, ShufflePermutation
from .regions import FullRegion, BackgroundRegion, ROIRegion

# Define a TypeVar for image-like inputs
ImageInput = TypeVar("ImageInput", sitk.Image, np.ndarray)


REGION_REGISTRY = {cls.region_name: cls for cls in [FullRegion, ROIRegion, BackgroundRegion]}

PERMUTATION_REGISTRY = {
	cls.permutation_name: cls for cls in [ShufflePermutation, SamplePermutation, RandomPermutation]
}


@dataclass
class NegativeControlManager:
	"""Manager class for applying negative control strategies to images."""

	permutation_strategies: List[PermutationStrategy] = field(default_factory=list)
	region_strategies: List[RegionStrategy] = field(default_factory=list)

	@classmethod
	def from_strings(
		cls,
		permutation_types: List[str],
		region_types: List[str],
		random_seed: Optional[int] = None,
	) -> "NegativeControlManager":
		"""Create a NegativeControlManager instance from string representations."""
		permutation_strategies = [
			PERMUTATION_REGISTRY[control_type](random_seed=random_seed)
			for control_type in permutation_types
		]

		region_strategies = [REGION_REGISTRY[region_type]() for region_type in region_types]

		return cls(
			permutation_strategies=permutation_strategies,
			region_strategies=region_strategies,
		)

	@property
	def strategy_products(self) -> Iterator[tuple[PermutationStrategy, RegionStrategy]]:
		"""Get all combinations of permutation and region strategies."""
		return product(self.permutation_strategies, self.region_strategies)

	def apply(
		self, base_image: ImageInput, mask: ImageInput
	) -> Iterator[tuple[ImageInput, str, str]]:
		"""Apply the permutation strategies to the region strategies."""
		for permutation_strategy, region_strategy in self.strategy_products:
			yield (
				permutation_strategy(base_image, mask, region_strategy),
				permutation_strategy.name(),
				region_strategy.name(),
			)

	def apply_single(
		self,
		base_image: ImageInput,
		mask: ImageInput,
		permutation_strategy: PermutationStrategy | str,
		region_strategy: RegionStrategy | str,
		random_seed: Optional[int] = None,
	) -> tuple[ImageInput, str, str]:
		"""Apply a single perturbation strategy to a single region strategy.

		Parameters
		----------
		base_image : np.ndarray | sitk.Image
			The base image to apply the negative control to.
		mask : np.ndarray | sitk.Image
			The mask image defining regions of interest.
		permutation_strategy : PermutationStrategy or str
			The permutation strategy to apply. Can be either a PermutationStrategy
			instance or a string name from PERMUTATION_REGISTRY.
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
		if isinstance(permutation_strategy, str):
			permutation_strategy = PERMUTATION_REGISTRY[permutation_strategy]()
		if isinstance(region_strategy, str):
			region_strategy = REGION_REGISTRY[region_strategy]()

		if random_seed is not None:
			permutation_strategy.random_seed = random_seed

		return (
			permutation_strategy(base_image, mask, region_strategy),
			permutation_strategy.name(),
			region_strategy.name(),
		)

	def __len__(self) -> int:
		"""Return the total number of strategy combinations."""
		return len(list(self.strategy_products))

	def __repr__(self) -> str:
		"""Return a string representation of the manager."""
		return f"NegativeControlManager(permutations={len(self.permutation_strategies)}, regions={len(self.region_strategies)})"
