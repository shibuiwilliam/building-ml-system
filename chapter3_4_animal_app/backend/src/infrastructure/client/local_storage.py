import os

from src.configurations import Configurations
from src.infrastructure.storage import AbstractStorage


class LocalStorage(AbstractStorage):
    def __init__(self):
        super().__init__()
        pass

    def make_photo_url(
        self,
        uuid: str,
    ) -> str:
        return os.path.join(Configurations.work_directory, f"{uuid}.jpg")

    def upload_image(
        self,
        uuid: str,
        source_file_path: str,
    ) -> str:
        photo_url = self.make_photo_url(uuid=uuid)
        return photo_url

    def download_image(
        self,
        uuid: str,
        destination_directory: str,
    ) -> str:
        return os.path.join(Configurations.work_directory, f"{uuid}.jpg")
