from logging import getLogger

logger = getLogger(__name__)


class BaseException(Exception):
    def __init__(self, message: str, detail: str):
        self.message = message
        self.detail = detail
