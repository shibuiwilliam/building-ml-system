import asyncio
import os
from io import BytesIO
from typing import List, Optional, Tuple

import httpx
import numpy as np
from PIL import Image
from src.dataset.data_manager import AbstractDBClient, AnimalRepository
from src.dataset.schema import Animal, Dataset, DownloadedImage, DownloadedImages
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


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
) -> Tuple[Optional[str], Optional[str]]:
    logger.info(f"download: {source_path} to {destination_path}")
    if os.path.exists(destination_path):
        logger.error(f"data already exists: {id} {source_path} {destination_path}")
        return id, destination_path
    res = await client.get(source_path)
    if res.status_code != 200:
        raise Exception(f"failed to download {source_path}")
    img = Image.open(BytesIO(res.content))
    if img.mode == "RGBA":
        img_rgb = Image.new("RGB", (img.height, img.width), (255, 255, 255))
        img_rgb.paste(img, mask=img.split()[3])
        img = img_rgb
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
            tasks.append(download_file(client, animal.id, animal.photo_url, d))
        data = await asyncio.gather(*tasks)
    downloaded_images = []
    for id, destination_path in data:
        if id is not None and destination_path is not None:
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
    logger.info("start downloading image")
    os.makedirs(destination_directory, exist_ok=True)
    loop = asyncio.get_event_loop()
    destination_paths = loop.run_until_complete(
        download_files(
            animals=animals,
            destination_directory=destination_directory,
        )
    )
    logger.info("done downloading image")
    return destination_paths


def load_images(
    images: DownloadedImages,
    height: int,
    width: int,
) -> Dataset:
    logger.info("start loading image")
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
        if len(ids) % 100 == 0:
            logger.info(f"loaded: {len(ids)} images")
    logger.info("done loading image")
    return Dataset(
        data=data,
        ids=ids,
    )
