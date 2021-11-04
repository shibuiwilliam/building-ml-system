import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.DEBUG)


def configure_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    return logger
