"""Module for managing file reading and writing."""

from .readers import NIFTIReader
from .writers import NIFTIWriter

__all__ = ["NIFTIWriter", "NIFTIReader"]
