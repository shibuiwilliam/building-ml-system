import os
from abc import ABC, abstractmethod
from logging import getLogger

from google.cloud import storage
from src.configurations import Configurations

logger = getLogger(__name__)


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


class GoogleCloudStorage(AbstractStorage):
    def __init__(self):
        super().__init__()

        self.client = storage.Client()
        self.bucket = self.client.bucket(Configurations.gcs_bucket)

    def make_photo_url(
        self,
        uuid: str,
    ) -> str:
        photo_url = f"https://storage.cloud.google.com/{Configurations.gcs_bucket}/images/{uuid}.jpg"
        return photo_url

    def upload_image(
        self,
        uuid: str,
        source_file_path: str,
    ) -> str:
        destination_blob_name = os.path.join("images", f"{uuid}.jpg")
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_path)
        photo_url = self.make_photo_url(uuid=uuid)
        return photo_url

    def download_image(
        self,
        uuid: str,
        destination_directory: str,
    ) -> str:
        source_blob_name = os.path.join("images", f"{uuid}.jpg")
        blob = self.bucket.blob(source_blob_name)
        destination_file_path = os.path.join(destination_directory, f"{uuid}.jpg")
        blob.download_to_filename(destination_file_path)
        return destination_file_path
