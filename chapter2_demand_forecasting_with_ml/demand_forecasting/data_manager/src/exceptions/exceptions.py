class BaseException(Exception):
    def __init__(self, message: str, detail: str):
        self.message = message
        self.detail = detail


class DatabaseException(BaseException):
    def __init__(self, message: str, detail: str):
        super().__init__(message=message, detail=detail)
        self.__message = f"database exception: {self.message}"

    def __str__(self):
        return self.__message
