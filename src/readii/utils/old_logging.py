import logging
import logging.config
import os
from typing import Optional

BASE_LOGGING: dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # 'json': {
        #     'class': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        #     'format': '%(asctime)s %(name)s %(levelname)s %(module)s %(message)s %(pathname)s %(lineno)s %(funcName)s %(threadName)s %(thread)s %(process)s %(processName)s',  # noqa: E501
        #     'datefmt': '%Y-%m-%d %H:%M:%S',
        # },
        'stdout': {
            'format': '%(asctime)s %(levelname)s: %(message)s (%(module)s:%(funcName)s:%(lineno)d)',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'stdout',
        },
    },
    'loggers': {
        'devel': {
            'handlers': ['console'],
            'level': os.getenv('READII_VERBOSITY', 'INFO'),
            'propagate': True,
        },
    },
}


def setup_logger(
    logger_name: str = 'root',
    config: Optional[dict] = None,
    extra_handlers: Optional[list] = None,
  ) -> logging.Logger:
    """Set up a logger with optional custom configuration and log file."""
    valid_loggers = ['devel', 'prod', 'root']
    assert (
        logger_name in valid_loggers
    ), f'Invalid logger name. Available options are {valid_loggers}'
    
    # Merge the base config with any custom config
    logging_config = BASE_LOGGING.copy()
    if config:
        logging_config.update(config)
    logging.config.dictConfig(logging_config)

    logger = logging.getLogger(logger_name)

    # Add any extra handlers provided
    if extra_handlers:
        for handler in extra_handlers:
            logger.addHandler(handler)

    return logger

def get_logger(config: Optional[dict] = None) -> logging.Logger:
    """Retrieve logger based on the environment, with an optional configuration."""
    env = os.getenv('READII_ENV', 'development')

    logger_name = 'devel' if env in ['devel', 'development'] else 'prod'
    return setup_logger(logger_name=logger_name, config=config)

# Example usage
if __name__ == "__main__":
    logger = get_logger()
    logger.info("This is an informational message.")
    logger.debug("This is a debug message.")
