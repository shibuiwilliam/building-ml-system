import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.DEBUG)


def configure_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] [%(funcName)s] %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
