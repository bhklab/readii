from readii.logging import logger
import click


@click.command()
def main():
    """
    Create and configure an example structlog logger.
    """
    logger.debug(
        "This is a debug message",
    )
    logger.info(
        "This is an info message",
    )
    logger.warning(
        "This is a warning message",
    )
    logger.error(
        "This is an error message",
    )
    logger.critical(
        "This is a critical message",
    )
    logger.fatal(
        "This is a fatal message",
    )

    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("This is an exception message")


if __name__ == "__main__":
    main()
