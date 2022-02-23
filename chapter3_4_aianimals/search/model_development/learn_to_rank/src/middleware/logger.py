import logging
import os
import sys

import cloudpickle

cloudpickle.register_pickle_by_value(sys.modules[__name__])

LOG_LEVEL = os.getenv("LOG_LEVEL", logging.DEBUG)


def configure_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)
    return logger
