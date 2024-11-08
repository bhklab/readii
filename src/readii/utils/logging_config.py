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


def json_formatter(x, __, event_dict):
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


class ESTTimeStamper:
    def __init__(self, fmt="%Y-%m-%dT%H:%M:%S%z"):
        self.fmt = fmt
        self.est = pytz.timezone("US/Eastern")

    def __call__(self, _, __, event_dict):
        now = datetime.datetime.now(self.est)
        event_dict["timestamp"] = now.strftime(self.fmt)
        return event_dict


# Rename old log files with creation date-time
def rename_old_log_file(file_path: Path):
    if file_path.exists():
        creation_time = datetime.datetime.fromtimestamp(file_path.stat().st_ctime)
        new_name = file_path.with_name(
            f"{file_path.stem}_{creation_time.strftime('%Y%m%d_%H%M%S')}{file_path.suffix}"
        )
        shutil.move(file_path, new_name)
    return file_path


def configure_logger(logfile: Path, LEVEL: str = "DEBUG", handlers: List[str] = ["console"]):
    """
    Configures the logging setup for the application using structlog and standard logging.

    This function sets up structlog to integrate with the standard library's logging module,
    configuring the logging formatters, handlers, and loggers as specified. It supports various
    logging outputs such as console, plain file, and JSON, each with customizable formats.

    Parameters
    ----------
    logfile : Path
        The path to the primary log file. This file will be used to log messages when the "file"
        or "json" handlers are specified.
    LEVEL : str, optional
        The logging level for the logger named 'readii'. This can be 'DEBUG', 'INFO', 'WARNING',
        'ERROR', or 'CRITICAL'. Default is 'DEBUG'.
    handlers : List[str], optional
        A list of handlers to use for logging. Possible values are "console", "file", and "json".
        Default is ["console"].

    Notes
    -----
    - The function renames old log files by appending their creation date-time before starting a new one.
    - All logs are time-stamped with Eastern Standard Time (EST).
    - Additional information such as module, function name, and line number can be recorded in the logs.
    - JSON logs are formatted with an indentation for better readability.
    """
    # if "file" in handlers or "json" in handlers:
    log_log = rename_old_log_file(logfile)
    log_json = rename_old_log_file(logfile.with_suffix(".json"))


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
        # if the log entry is not from structlog.
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
                                width=-1, 
                                show_locals=False
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
                            colors=False,
                            exception_formatter=structlog.dev.plain_traceback,
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
                        structlog.processors.JSONRenderer(
                            serializer=json.dumps, indent=2
                        ),
                    ],
                    "foreign_pre_chain": pre_chain,
                },
            },
            "handlers": {
                "console": {
                    # "level": LEVEL,
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                },
                "file": {
                    # "level": LEVEL,
                    "class": "logging.handlers.WatchedFileHandler",
                    "filename": log_log,
                    "formatter": "plain_file",
                },
                "json": {
                    # "level": LEVEL,
                    "class": "logging.handlers.WatchedFileHandler",
                    "filename": log_json,
                    "formatter": "json",
                },
            },
            "loggers": {
                "": {
                    "handlers": [],
                    "level": "ERROR",
                    "propagate": True,
                },
                "readii": {
                    "handlers" : handlers,
                    "level": LEVEL,
                    "propagate" : False
                }
            },
        }
    )
    structlog.configure_once(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=False,
    )


def get_logger(
    logfile_path: Path | str, level: str = "WARNING", handlers: List[str] = ["console"]
) -> structlog.stdlib.BoundLogger:
    """
    Retrieve a structlog logger with a specified log file path and logging level.

    This function configures and returns a structlog logger. It ensures that the log file path is correctly set up,
    creating necessary directories if they do not exist. The logger is configured to log messages to a file and
    to the console, with the specified logging level.

    Parameters
    ----------
    logfile_path : Path | str
        The path to the log file. This can be an absolute path or a relative path.
        - If the path is an absolute path, the log file will be created in that directory with the name 'readii.log'.
        - If the path is a relative path, the log file will be created in the current working directory under a 'logs' directory.
        - If the path does not have a '.log' suffix, it will be added automatically.
    level : str
        The logging level. This can be one of the standard logging levels: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
        Default is 'DEBUG'.

    Returns
    -------
    structlog.stdlib.BoundLogger
        A configured structlog logger instance.

    Raises
    ------
    PermissionError
        If the function does not have permission to create the log file or directories.

    Notes
    -----
    - If the log file path is not absolute, it will be created in the current working directory under a 'logs' directory.
    - If the log file path is a directory and exists, the log file will be created in that directory with the name 'readii.log'.
    - If the log file path does not have a '.log' suffix, it will be added automatically.
    - The function ensures that the logger is configured only once using `structlog.is_configured()`.

    Examples
    --------
    >>> logger = get_logger("my_log.log", "INFO")
    >>> logger.info("This is an informational message.")
    """
    if structlog.is_configured():
        structlog.reset_defaults()

    LOGFILE_NAME = Path(logfile_path)

    if LOGFILE_NAME.is_dir():
        logfile = LOGFILE_NAME / "readii.log"
    elif not LOGFILE_NAME.suffix == ".log":
        logfile = LOGFILE_NAME.with_suffix(".log")
    else:
        logfile = Path.cwd() / "logs" / LOGFILE_NAME
    try:
        logfile.parent.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print(f"PermissionError: Cannot create log file {logfile}")
        sys.exit(1)
    
    configure_logger(logfile.absolute(), level, handlers)

    logger = structlog.get_logger("readii")
    return logger


logger = get_logger("readii.log", "DEBUG")