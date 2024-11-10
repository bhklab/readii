# Structlog-Based Logging Setup

This logging module uses `structlog` to enable structured, customizable logging,
supporting JSON and console formats based on output type (TTY vs. non-TTY). The
setup is flexible, with processors to format paths, timestamps, and call site
details for enhanced readability.

## Key Components

1. **LoggingManager**: Initializes the logger based on output preference.
   - JSON format (machine-readable) for structured logging.
   - Console format (human-readable) for development.
   - Uses custom processors for path prettification, EST timestamps, and call
     information.

2. **Custom Processors**:
   - **PathPrettifier**: Converts absolute paths to relative paths based on a
     base directory.
   - **ESTTimeStamper**: Adds an EST timestamp with configurable format.
   - **CallPrettifier**: Formats module, function, and line number details.
   - **JSONFormatter**: Organizes core and extra fields for clean JSON output.

## Usage Example

```python
# Initialize the logger
from readii.logging import logger

# Log a sample message
logger.info("This is an info message", extra_field="extra_value")

# Sample Output:
# JSON (non-TTY):
# {
#   "event": "This is an info message",
#   "level": "info",
#   "timestamp": "2024-11-10T12:00:00-0500",
#   "call": "module.function:line_number",
#   "extra": {"extra_field": "extra_value"}
# }

# Console (TTY):
# 2024-11-10T12:00:00-0500 [info] module.function:line_number - This is an info
# message
#     extra_field="extra_value"
```