from abc import ABC, abstractmethod
from logging import getLogger

from cryptography.fernet import Fernet

logger = getLogger(__name__)


class AbstractCrypt(ABC):
    def __init__(
        self,
        key_file_path: str,
    ):
        self._key_file_path = key_file_path

    @abstractmethod
    def encrypt(
        self,
        text: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(
        self,
        enc_text: str,
    ) -> str:
        raise NotImplementedError


class Crypt(AbstractCrypt):
    def __init__(
        self,
        key_file_path: str,
    ):
        super().__init__(key_file_path=key_file_path)
        self.__load_key()
        self.__initialize()

    def __initialize(self):
        self.__fernet = Fernet(self.__key)

    def __load_key(self):
        with open(self._key_file_path, "rb") as f:
            self.__key = f.read()

    def encrypt(
        self,
        text: str,
    ) -> str:
        enc_text = self.__fernet.encrypt(text.encode()).decode()
        return enc_text

    def decrypt(
        self,
        enc_text: str,
    ) -> str:
        text = self.__fernet.decrypt(enc_text.encode()).decode()
        return text
