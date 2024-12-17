"""BaseWriter Module.

BaseWriter Module
-----------------

This module provides a reusable and extensible base class, `BaseWriter`, for managing file writing operations 
with customizable paths and filenames. It is designed for developers who need to implement file-writing 
solutions across a variety of file types and applications.

The `BaseWriter` class simplifies the creation, validation, and management of file paths, allowing developers 
to focus on implementing the logic specific to their file-writing use case.

Overview
--------

The `BaseWriter` uses a filename format string and a root directory to generate file paths dynamically. 
It ensures the necessary directories exist (or are created if requested) and provides built-in support 
for adding timestamps or other dynamic placeholders in filenames.

The key components include:
- **Dynamic Filename Resolution**: Uses a customizable filename format string and parameters provided 
  at runtime to generate paths dynamically.
- **Directory Management**: Automatically creates directories when needed and cleans up empty directories 
  in case of failures or unused resources.
- **Context Management**: Supports `with`-statements for seamless resource management.
- **Subclassing Support**: Designed as an abstract base class (ABC), requiring subclasses to implement 
  the `save()` method for writing data.

---

Key Features
------------

1. **Flexible Filename Patterns**:
  - Placeholders can be included in the `filename_format` string to dynamically generate filenames.
  - Automatically injects date and time strings (`date`, `time`, `date_time`).

2. **Directory Management**:
  - Ensures directories exist before saving files.
  - Optionally removes empty directories on context manager exit.

3. **Context Management**:
  - Automatically handles setup and cleanup when used in a `with` block.

4. **Easy Extension**:
  - Developers can create subclasses by implementing a `save()` method specific to the data format.

---

How to Use
----------

To use `BaseWriter`, follow these steps:

1. **Inherit from `BaseWriter`**:
  Create a new class that inherits from `BaseWriter` and implements the abstract `save()` method.

2. **Define Your Save Logic**:
  The `save()` method should handle the logic for writing data to a file.

3. **Specify Filename Format**:
  Use a format string for `filename_format` with placeholders such as `{key}` or `%key`.

4. **Provide Parameters**:
  Pass the required parameters at runtime to resolve the placeholders in the filename format.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import TracebackType
from typing import Any, Optional

from readii.io.utils import PatternResolver
from readii.utils import logger


@dataclass
class BaseWriter(ABC):
	"""Abstract base class for managing file writing with customizable paths and filenames.

	Attributes
	----------
	root_directory : Path
		The root directory where files will be saved.
	filename_format : str
		The format string for generating filenames.
	create_dirs : bool, optional
		Whether to create directories if they do not exist (default is True).
	pattern_resolver : PatternResolver
		Instance for resolving filename patterns.

	Methods
	-------
	save(*args, **kwargs)
		Abstract method for writing data. Must be implemented by subclasses.
	resolve_path(**kwargs)
		Generate a file path based on the filename format and additional parameters.
	__enter__()
		Enter the runtime context related to this writer.
	__exit__(exc_type, exc_value, traceback)
		Exit the runtime context related to this writer.
	"""

	# Any subclass has to be initialized with a root directory and a filename format
	root_directory: Path
	filename_format: str

	# optionally, you can set create_dirs to False if you want to handle the directory creation yourself
	create_dirs: bool = field(default=True)

	# class-level pattern resolver instance shared across all instances
	pattern_resolver: PatternResolver = field(init=False)

	def __post_init__(self) -> None:
		"""
		Initialize the writer with the given root directory and filename format.

		Raises
		------
		FileNotFoundError
			If create_dirs is False and the root directory does not exist.
		"""
		self.root_directory = Path(self.root_directory)
		if self.create_dirs:
			self.root_directory.mkdir(parents=True, exist_ok=True)
		elif not self.root_directory.exists():
			msg = f"Root directory {self.root_directory} does not exist."
			raise FileNotFoundError(msg)
		self.pattern_resolver = PatternResolver(self.filename_format)

	@abstractmethod
	def save(self, *args: Any, **kwargs: Any) -> Path: # noqa
		"""Abstract method for writing data. Must be implemented by subclasses.

		Returns
		-------
		Path
			The path to the saved file.
		"""
		pass

	def _generate_datetime_strings(self) -> dict[str, str]:
		now = datetime.now(timezone.utc)
		return {
			"date": now.strftime("%Y-%m-%d"),
			"time": now.strftime("%H%M%S"),
			"date_time": now.strftime("%Y-%m-%d_%H%M%S"),
		}

	def resolve_path(self, **kwargs: Any) -> Path: # noqa
		"""Generate a file path based on the filename format and additional parameters.

		Parameters
		----------
		**kwargs : dict
			Additional parameters for filename generation.

		Returns
		-------
		Path
			The resolved file path.
		"""
		context = {**self._generate_datetime_strings(), **kwargs}
		filename = self.pattern_resolver.resolve(context)
		out_path = self.root_directory / filename
		if self.create_dirs:
			out_path.parent.mkdir(parents=True, exist_ok=True)
		return out_path

	# Context Manager Implementation
	def __enter__(self) -> "BaseWriter":
		"""Enter the runtime context related to this writer.

		Useful if the writer needs to perform setup actions, such as
		opening connections or preparing resources.

		Returns
		-------
		BaseWriter
			The writer instance itself.
		"""
		logger.debug(f"Entering context manager for {self.__class__.__name__}")
		return self

	def __exit__(
		self: "BaseWriter",
		exc_type: Optional[type],
		exc_value: Optional[BaseException],
		traceback: Optional[TracebackType],
	) -> None:
		"""Exit the runtime context related to this writer.

		Parameters
		----------
		exc_type : Optional[type]
			The exception type, if an exception was raised, otherwise None.
		exc_value : Optional[BaseException]
			The exception instance, if an exception was raised, otherwise None.
		traceback : Optional[Any]
			The traceback object, if an exception was raised, otherwise None.
		"""
		if exc_type:
			logger.exception(
				f"Exception raised in {self.__class__.__name__} while in context manager.",
				exc_info=exc_value,
			)
		logger.debug(f"Exiting context manager for {self.__class__.__name__}")

		# if the root directory is empty, aka we created it but didn't write anything, delete it
		if (
			self.create_dirs
			and self.root_directory.exists()
			and not any(self.root_directory.iterdir())
		):
			logger.debug(f"Deleting empty directory {self.root_directory}")
			self.root_directory.rmdir()  # remove the directory if it's empty
