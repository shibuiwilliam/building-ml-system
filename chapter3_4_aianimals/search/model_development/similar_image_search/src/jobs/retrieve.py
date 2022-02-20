import asyncio
import os
from io import BytesIO
from typing import List, Tuple

import httpx
import numpy as np
from PIL import Image
from src.dataset.data_manager import AbstractDBClient, AnimalRepository
from src.dataset.schema import Animal, Dataset, DownloadedImage, DownloadedImages


def retrieve_animals(
    db_client: AbstractDBClient,
) -> List[Animal]:
    animal_repository = AnimalRepository(db_client=db_client)
    return animal_repository.select_all()


async def download_file(
    client: httpx.AsyncClient,
    id: str,
    source_path: str,
    destination_path: str,
) -> Tuple[str, str]:
    if os.path.exists(destination_path):
        return destination_path
    res = await client.get(source_path)
    if res.status_code != 200:
        raise Exception(f"failed to download {source_path}")
    img = Image.open(BytesIO(res.content))
    img.save(destination_path)
    return id, destination_path


async def download_files(
    animals: List[Animal],
    destination_directory: str,
) -> DownloadedImages:
    tasks = []
    timeout = 10.0
    transport = httpx.AsyncHTTPTransport(
        retries=3,
    )
    async with httpx.AsyncClient(
        timeout=timeout,
        transport=transport,
    ) as client:
        for animal in animals:
            basename = os.path.basename(animal.photo_url)
            d = os.path.join(destination_directory, basename)
            tasks.append(download_file(client, animal.photo_url, d))
        ids, destination_paths = await asyncio.gather(*tasks)
    downloaded_images = []
    for id, destination_path in zip(ids, destination_paths):
        downloaded_images.append(
            DownloadedImage(
                id=id,
                path=destination_path,
            )
        )
    return DownloadedImages(images=downloaded_images)


def download_dataset(
    animals: List[Animal],
    destination_directory: str,
) -> DownloadedImages:
    loop = asyncio.get_event_loop()
    destination_paths = loop.run_until_complete(
        download_files(
            animals=animals,
            destination_directory=destination_directory,
        )
    )
    return destination_paths


def load_images(
    images: DownloadedImages,
    height: int,
    width: int,
) -> Dataset:
    data = np.zeros((len(images.images), height, width, 3)).astype(np.float32)
    ids = []
    for i, image in enumerate(images.images):
        img = Image.open(image.path)
        img_resized = img.resize((height, width))
        if img_resized.mode == "RGBA":
            img_rgb = Image.new("RGB", (height, width), (255, 255, 255))
            img_rgb.paste(img_resized, mask=img_resized.split()[3])
            img_resized = img_rgb
        img_array = np.array(img_resized).astype(np.float32) / 255.0
        data[i] = img_array
        ids.append(image.id)
    return Dataset(
        data=data,
        ids=ids,
    )
