from dataclasses import dataclass
from pathlib import Path
from typing import List


# Define custom exceptions
class DirectoryScannerError(Exception):
	"""Base exception for errors in directory scanning."""
  
	pass

@dataclass
class DirectoryScanner:
	"""Handles scanning directories for files or subdirectories."""

	root_directory: Path
	include_files: bool = True
	include_directories: bool = False
	glob_pattern: str = "*"
	recursive: bool = True

	def scan(self) -> List[Path]:
		"""
		Scan the root directory for files and/or directories.

		Returns
		-------
		List[Path]
			A list of paths matching the criteria.
		"""
		if not self.root_directory.exists():
			msg = f"Root directory {self.root_directory} does not exist."
			raise DirectoryScannerError(msg)
		if not self.root_directory.is_dir():
			msg = f"Root directory {self.root_directory} is not a directory."
			raise DirectoryScannerError(msg)

		if self.recursive:
			paths = self.root_directory.rglob(self.glob_pattern)
		else:
			paths = self.root_directory.glob(self.glob_pattern)

		if self.include_files and self.include_directories:
			return list(paths)
		elif self.include_files:
			return [p for p in paths if p.is_file()]
		elif self.include_directories:
			return [p for p in paths if p.is_dir()]
		return []
