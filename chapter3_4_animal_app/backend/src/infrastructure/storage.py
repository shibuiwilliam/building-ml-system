from abc import ABC, abstractmethod


class AbstractStorage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def make_photo_url(
        self,
        uuid: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def upload_image(
        self,
        uuid: str,
        source_file_path: str,
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def download_image(
        self,
        uuid: str,
        destination_directory: str,
    ) -> str:
        raise NotImplementedError
