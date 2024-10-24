"""Definitions for negative control types used in the radiomics analysis."""

from enum import Enum, auto
from typing import Any, Type


class NegativeControlType(Enum):
    """Enumeration of negative control types used in radiomics analysis.

    - SHUFFLED: TODO::
    - RANDOMIZED: TODO::
    - RANDOMIZED_SAMPLED: TODO::
    """

    SHUFFLED = auto()
    RANDOMIZED = auto()
    RANDOMIZED_SAMPLED = auto()


class NegativeControlRegion(Enum):
    """Enumeration of regions for applying negative controls in radiomics.

    - FULL: TODO::
    - ROI: TODO::
    - NON_ROI: TODO::
    """

    FULL = auto()
    ROI = auto()
    NON_ROI = auto()

    @classmethod
    def _missing_(cls, value) -> 'NegativeControlRegion':
        if isinstance(value, str):
            lowercase_value = value.lower()
            for member in cls:
                if member.name.lower() == lowercase_value:
                    return member
        return super()._missing_(value)
