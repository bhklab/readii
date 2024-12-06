from dataclasses import dataclass
from itertools import product
from typing import Iterator, List, Optional, TypeVar

from .abstract_classes import NegativeControlStrategy, RegionStrategy
from .negative_controls import RandomizedControl, SampledControl, ShuffledControl
from .regions import FullRegion, NonROIRegion, ROIRegion

T = TypeVar("T")


REGION_REGISTRY = {
  cls.region_name: cls
  for cls in [FullRegion, ROIRegion, NonROIRegion]
}

NEGATIVE_CONTROL_REGISTRY = {
  cls.negative_control_name: cls
  for cls in [ShuffledControl, SampledControl, RandomizedControl]
}

@dataclass
class NegativeControlManager:
	"""Manager class for applying negative control strategies to images."""

	negative_control_strategies: List[NegativeControlStrategy]
	region_strategies: List[RegionStrategy]

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

		region_strategies = [
			REGION_REGISTRY[region_type]()
			for region_type in region_types
		]

		return cls(
			negative_control_strategies=negative_control_strategies,
			region_strategies=region_strategies,
		)

	@property
	def strategy_products(self) -> Iterator[tuple[NegativeControlStrategy, RegionStrategy]]:
		"""Get all combinations of negative control and region strategies."""
		return product(self.negative_control_strategies, self.region_strategies)

	def apply(self, base_image: T, mask: T) -> Iterator[tuple[T, str, str]]:
		"""Apply the negative control strategies to the region strategies."""
		for control_strategy, region_strategy in self.strategy_products:
			yield (
				control_strategy(base_image, mask, region_strategy),
				control_strategy.name(),
				region_strategy.name(),
			)

	def apply_single(self, base_image: T, mask: T, control_strategy: NegativeControlStrategy, region_strategy: RegionStrategy) -> tuple[T, str, str]:
		"""Apply a single negative control strategy to a single region strategy."""
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