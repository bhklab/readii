"""Module for negative control strategies and region strategies."""

from .abstract_classes import NegativeControlStrategy, RegionStrategy
from .manager import NEGATIVE_CONTROL_REGISTRY, REGION_REGISTRY, NegativeControlManager
from .negative_controls import RandomizedControl, SampledControl, ShuffledControl
from .regions import FullRegion, NonROIRegion, ROIRegion

__all__ = [
	"RegionStrategy",
	"NegativeControlStrategy",
	"FullRegion",
	"ROIRegion",
	"NonROIRegion",
	"ShuffledControl",
	"SampledControl",
	"RandomizedControl",
	"REGION_REGISTRY",
	"NEGATIVE_CONTROL_REGISTRY",
	"NegativeControlManager",
]
