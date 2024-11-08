import structlog
import logging
import logging.config
import json
from structlog.typing import Processor
from typing import Optional, List, Union
from pathlib import Path
import sys
from structlog.processors import CallsiteParameter
import shutil
import datetime
import pytz
class ESTTimeStamper:
    def __init__(self, fmt="%Y-%m-%dT%H:%M:%S%z"):
        self.fmt = fmt
        self.est = pytz.timezone("US/Eastern")

    def __call__(self, _, __, event_dict):
        now = datetime.datetime.now(self.est)
        event_dict["timestamp"] = now.strftime(self.fmt)
        return event_dict


# Create logs directory if it doesn't exist
log_dir = Path("./logs")
log_dir.mkdir(parents=True, exist_ok=True)


# Rename old log files with creation date-time
def rename_old_log_file(file_path: Path):
    if file_path.exists():
        creation_time = datetime.datetime.fromtimestamp(file_path.stat().st_ctime)
        new_name = file_path.with_name(
            f"{file_path.stem}_{creation_time.strftime('%Y%m%d_%H%M%S')}{file_path.suffix}"
        )
        shutil.move(file_path, new_name)


rename_old_log_file(log_dir / "test.log")
rename_old_log_file(log_dir / "test.json")


def path_prettifier(base_dir: Optional[Path] = None):
    base_dir = base_dir or Path.cwd()

    def processor(_, __, event_dict):
        for key, path in event_dict.items():
            if not isinstance(path, Path):
                continue
            try:
                path = path.relative_to(base_dir)
            except ValueError:
                pass  # path is not relative to cwd
            event_dict[key] = f"{str(path)}"
        return event_dict

    return processor


def json_formatter(_, __, event_dict):
    core_fields = {"event", "level", "timestamp", "exception"}

    call = {
        "module": event_dict.pop("module", ""),
        "func_name": event_dict.pop("func_name", ""),
        "lineno": event_dict.pop("lineno", ""),
    }

    extra_fields = {
        key: value for key, value in event_dict.items() if key not in core_fields
    }
    for key in extra_fields:
        del event_dict[key]

    event_dict["extra"] = extra_fields
    event_dict["call"] = call
    return event_dict


def call_prettifier(_, __, event_dict):
    call = {
        "module": event_dict.pop("module", ""),
        "func_name": event_dict.pop("func_name", ""),
        "lineno": event_dict.pop("lineno", ""),
    }
    # event_dict["call"] = f"{call.module}.{call.func_name}:{call.lineno}"
    event_dict["call"] = f"{call['module']}.{call['func_name']}:{call['lineno']}"

    return event_dict


extra_processors: List[Processor] = [
    structlog.processors.CallsiteParameterAdder(
        [
            CallsiteParameter.MODULE,
            CallsiteParameter.FUNC_NAME,
            CallsiteParameter.LINENO,
        ]
    ),
]

timestamper = ESTTimeStamper(fmt="%Y-%m-%dT%H:%M:%S%z")
pre_chain = [
    # Add the log level and a timestamp to the event_dict if the log entry
    # is not from structlog.
    structlog.stdlib.add_log_level,
    # Add extra attributes of LogRecord objects to the event dictionary
    # so that values passed in the extra parameter of log methods pass
    # through to log output.
    structlog.stdlib.ExtraAdder(),
    timestamper,
]


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    *extra_processors,
                    path_prettifier(),
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    call_prettifier,
                    structlog.dev.ConsoleRenderer(
                        exception_formatter=structlog.dev.RichTracebackFormatter(
                            width=-1, show_locals=False
                        )
                    ),
                ],
                "foreign_pre_chain": pre_chain,
            },
            "plain_file": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    *extra_processors,
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(
                        colors=False, exception_formatter=structlog.dev.plain_traceback
                    ),
                ],
                "foreign_pre_chain": pre_chain,
            },
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    *extra_processors,
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.processors.dict_tracebacks,
                    structlog.processors.format_exc_info,
                    json_formatter,
                    structlog.processors.JSONRenderer(serializer=json.dumps, indent=4),
                ],
                "foreign_pre_chain": pre_chain,
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": log_dir / "test.log",
                "formatter": "plain_file",
            },
            "json": {
                "level": "DEBUG",
                "class": "logging.handlers.WatchedFileHandler",
                "filename": log_dir / "test.json",
                "formatter": "json",
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file", "json"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }
)

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

# logger = structlog.get_logger()


def get_logger() -> structlog.stdlib.BoundLogger:
    """Retrieve a structlog logger."""
    return structlog.get_logger()
