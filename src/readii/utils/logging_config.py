import structlog
from structlog.typing import Processor
from typing import Optional, List, Union
import sys
from structlog.processors import CallsiteParameter
from pathlib import Path
import json
from structlog.contextvars import (
    bind_contextvars,
    bound_contextvars,
    clear_contextvars,
    merge_contextvars,
    unbind_contextvars,
)

class PathPrettifier:
    """A processor for printing paths.

    Changes all pathlib.Path objects.

    1. Remove PosixPath(...) wrapper by calling str() on the path.
    2. If path is relative to current working directory,
       print it relative to working directory.

    Note that working directory is determined when configuring structlog.
    """

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()

    def __call__(self, _, __, event_dict):
        for key, path in event_dict.items():
            if not isinstance(path, Path):
                continue
            path = event_dict[key]
            try:
                path = path.relative_to(self.base_dir)
            except ValueError:
                pass  # path is not relative to cwd
            event_dict[key] = str(path)

        return event_dict

def callsite_formatter(_, __, event_dict):
    module = event_dict.pop('module', '')
    func_name = event_dict.pop('func_name', '')
    lineno = event_dict.pop('lineno', '')
    event_dict['call'] = f"{module}:{func_name}:{lineno}"
    return event_dict

# to print the callside like (loaders:loadRTSTRUCTSITK:90) 
# we need to add that info to the event_dict, then run callsite_formatter which removes the info 
# and formats it for the event_dict
extra_processors: List[Processor] = [
    structlog.processors.CallsiteParameterAdder([
        CallsiteParameter.MODULE,
        CallsiteParameter.FUNC_NAME,
        CallsiteParameter.LINENO,
    ]),
    callsite_formatter,
]


shared_processors: list[Processor] =[
    structlog.processors.TimeStamper(fmt="%y-%m-%d %H:%M:%S"),
    structlog.processors.add_log_level,
]


shared_processors = shared_processors + extra_processors

if not sys.stdout.isatty():
    processors = shared_processors + [
        structlog.dev.ConsoleRenderer(
            colors=False,
            exception_formatter=structlog.dev.plain_traceback
        ),
    ]
elif sys.stderr.isatty() and sys.stdout.isatty():
    processors = shared_processors + [
        PathPrettifier(),
        structlog.dev.ConsoleRenderer(
            exception_formatter=structlog.dev.rich_traceback,
        ),
    ]

if not sys.stderr.isatty():
    processors = shared_processors + [
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(serializer=json.dumps, indent=4),
    ]

structlog.configure(
    processors=processors,
)

logger = structlog.get_logger()

def get_logger() -> structlog.stdlib.BoundLogger:
    """Retrieve a structlog logger."""
    return structlog.get_logger()

if __name__ == "__main__":
    initfile = Path(__file__).parent / "__init__.py"

    logger.info("This is an informational message.", initfile=initfile)