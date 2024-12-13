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
	"""Abstract base class for managing file writing with customizable paths and filenames."""

	# Any subclass has to be initialized with a root directory and a filename format
	root_directory: Path
	filename_format: str

	# optionally, you can set create_dirs to False if you want to handle the directory creation yourself
	create_dirs: bool = field(default=True)

	# class-level pattern resolver instance shared across all instances
	pattern_resolver: PatternResolver = field(init=False)

	def __post_init__(self) -> None:
		"""Initialize the writer with the given root directory and filename format."""
		self.root_directory = Path(self.root_directory)
		if self.create_dirs:
			self.root_directory.mkdir(parents=True, exist_ok=True)
		elif not self.root_directory.exists():
			msg = f"Root directory {self.root_directory} does not exist."
			raise FileNotFoundError(msg)
		self.pattern_resolver = PatternResolver(self.filename_format)

	@abstractmethod
	def save(self, *args: Any, **kwargs: Any) -> Path:  # noqa
		"""Abstract method for writing data. Must be implemented by subclasses."""
		pass

	def _generate_datetime_strings(self) -> dict[str, str]:
		now = datetime.now(timezone.utc)
		return {
			"date": now.strftime("%Y-%m-%d"),
			"time": now.strftime("%H%M%S"),
			"date_time": now.strftime("%Y-%m-%d_%H%M%S"),
		}

	def resolve_path(self, **kwargs: Any) -> Path:  # noqa
		"""Generate a file path based on the filename format, subject ID, and additional parameters."""
		context = {**self._generate_datetime_strings(), **kwargs}
		filename = self.pattern_resolver.resolve(context)
		out_path = self.root_directory / filename
		if self.create_dirs:
			out_path.parent.mkdir(parents=True, exist_ok=True)
		return out_path

	# Context Manager Implementation
	def __enter__(self) -> "BaseWriter":
		"""
		Enter the runtime context related to this writer.

		Useful if the writer needs to perform setup actions, such as
		opening connections or preparing resources.
		"""
		logger.debug(f"Entering context manager for {self.__class__.__name__}")
		return self

	def __exit__(
		self: "BaseWriter",
		exc_type: Optional[type],
		exc_value: Optional[BaseException],
		traceback: Optional[TracebackType],
	) -> None:
		"""
		Exit the runtime context related to this writer.

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
