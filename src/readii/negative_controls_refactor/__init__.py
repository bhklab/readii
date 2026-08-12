"""Module for negative control strategies and region strategies."""

from .abstract_classes import PermutationStrategy, RegionStrategy
from .manager import PERMUTATION_REGISTRY, REGION_REGISTRY, NegativeControlManager
from .permutations import RandomPermutation, SamplePermutation, ShufflePermutation
from .regions import FullRegion, BackgroundRegion, ROIRegion

__all__ = [
	"RegionStrategy",
	"PermutationStrategy",
	"FullRegion",
	"ROIRegion",
	"BackgroundRegion",
	"ShufflePermutation",
	"SamplePermutation",
	"RandomPermutation",
	"REGION_REGISTRY",
	"PERMUTATION_REGISTRY",
	"NegativeControlManager",
]
