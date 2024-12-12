from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Union

FileDict = Dict[str, Union[Path, str]]

# Define custom exceptions
class FileFilterError(Exception):
	"""Base exception for errors in file filtering."""
	
	pass


class FileFilter:
	"""Filters a list of dictionaries based on provided keyword arguments or a list of filters."""

	@staticmethod
	def filter(files: List[FileDict], filters: List[Dict[str, Any]] | None = None, **kwargs: Any) -> List[FileDict]: # noqa
		"""
		Apply filters to a list of dictionaries.

		Parameters
		----------
		files : List[Dict[str, Any]]
			The list of dictionaries to filter.
		filters : List[Dict[str, Any]], optional
			A list of dictionaries specifying filter criteria.
		kwargs : Any
			Keyword arguments to filter the dictionaries by.

		Returns
		-------
		List[Dict[str, Any]]
			A list of dictionaries that match the filter criteria.
		"""
		filtered_files = files

		def matches_criteria(file: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
			for key, value in criteria.items():
				if isinstance(value, list):
					if file.get(key) not in value:
						return False
				elif callable(value):
					if not value(file.get(key)):
						return False
				elif file.get(key) != value:
					return False
			return True

		if filters:
			for filter_criteria in filters:
				filtered_files = [file for file in filtered_files if matches_criteria(file, filter_criteria)]

		if kwargs:
			filtered_files = [file for file in filtered_files if matches_criteria(file, kwargs)]

		return filtered_files


@dataclass
class FilteredFiles:
	"""A container class for filtering collections of files based on specified criteria.

	Attributes
	----------
		files: A list of dictionaries containing file information with Path or string values.
	"""

	files: List[FileDict]

	def filter(self, filters: List[Dict[str, Any]] | None = None, **kwargs: Any) -> FilteredFiles: # noqa
		filtered_files = FileFilter.filter(self.files, filters=filters, **kwargs)
		return FilteredFiles(files=filtered_files)

	def __len__(self) -> int: # noqa
		return len(self.files)

	def __iter__(self) -> Iterator[FileDict]: # noqa
		return iter(self.files)