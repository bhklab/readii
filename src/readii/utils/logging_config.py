from imgtools.logging import get_logger
import os
DEFAULT_LOGGING_LEVEL = os.environ.get('READII_LOG_LEVEL', None) or 'WARNING'
logger = get_logger('readii', DEFAULT_LOGGING_LEVEL)
