import os
import shutil
from typing import Dict

from google.cloud import storage


def download_images_from_bucket(
    bucket_name: str,
    destination_directory: str,
):
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)
    for blob in blobs:
        destination_file_path = os.path.join(destination_directory, blob.name)
        _d = os.path.dirname(destination_file_path)
        os.makedirs(_d, exist_ok=True)
        blob.download_to_filename(destination_file_path)


def distribute_file_to_classname(
    classname_dict: Dict,
    source_directory: str,
):
    for v in classname_dict.values():
        s = os.path.join(source_directory, v["filename"])
        d = os.path.join(source_directory, str(v["subcategory"]))
        os.makedirs(d, exist_ok=True)
        shutil.move(s, d)
