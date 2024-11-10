"""
This module provides a logging setup using structlog with custom processors for path prettification,
call information formatting, and timestamping in Eastern Standard Time.

Usage:
    Import the logger and use it to log messages in your package.

    from readii.logging import logger

    logger.info("This is an info message", extra_field="extra_value")

    The logger can output in JSON format or console format based on whether the output is a TTY.

    - JSON output: Suitable for structured logging and machine parsing.
    - Console output: Suitable for human-readable logs during development.

Classes:
    LoggingManager: Manages the configuration and initialization of the logger.
"""

import structlog
import json as jsonlib
import sys

from structlog.processors import CallsiteParameterAdder, CallsiteParameter

from readii.logging.processors import (
    PathPrettifier,
    ESTTimeStamper,
    CallPrettifier,
)
from pathlib import Path
from typing import Optional


class LoggingManager:
    """
    Manages the configuration and initialization of the logger.

    Args:
        json_output (bool): Whether to output logs in JSON format. Defaults to False.
        base_dir (Optional[Path]): The base directory for path prettification. Defaults to the current working directory.
    """

    def __init__(self, json_output: bool = False, base_dir: Optional[Path] = None):
        self.json_output = json_output
        self.base_dir = base_dir or Path.cwd()
        self.logger = None
        self._initialize_logger()

    def _initialize_logger(self):
        """
        Initializes the logger with the appropriate processors based on the output format.
        """
        processors = [
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="ISO8601"),
            ESTTimeStamper(),
            PathPrettifier(base_dir=self.base_dir),
            CallsiteParameterAdder(
                [
                    CallsiteParameter.MODULE,
                    CallsiteParameter.FUNC_NAME,
                    CallsiteParameter.LINENO,
                ]
            ),
            structlog.processors.StackInfoRenderer(),
        ]

        if self.json_output:
            processors += [
                CallPrettifier(concise=False),
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(serializer=jsonlib.dumps, indent=2),
            ]
        else:
            processors += [
                CallPrettifier(concise=True),
                structlog.dev.ConsoleRenderer(
                    exception_formatter=structlog.dev.RichTracebackFormatter(
                        width=-1, show_locals=False
                    )
                ),
            ]

        structlog.configure(processors=processors)
        self.logger = structlog.get_logger()

    def get_logger(self) -> structlog.BoundLogger:
        """
        Returns the initialized logger.

        Returns:
            structlog.BoundLogger: The initialized logger.

        Raises:
            RuntimeError: If the logger has not been initialized.
        """
        if not self.logger:
            raise RuntimeError("Logger has not been initialized.")
        return self.logger


if sys.stdout.isatty():
    logging_manager = LoggingManager(json_output=False)
else:
    logging_manager = LoggingManager(json_output=True)

logger = logging_manager.get_logger()
