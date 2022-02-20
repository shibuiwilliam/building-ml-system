import asyncio
import os
from io import BytesIO
from typing import List

import httpx
from PIL import Image
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


async def download_file(
    client: httpx.AsyncClient,
    source_path: str,
    destination_path: str,
) -> str:
    logger.info(f"download {source_path}: {destination_path}")
    if os.path.exists(destination_path):
        return destination_path
    res = await client.get(source_path)
    if res.status_code != 200:
        raise Exception(f"failed to download {source_path}")
    img = Image.open(BytesIO(res.content))
    if img.mode == "RGBA":
        img_rgb = Image.new("RGB", (img.height, img.width), (255, 255, 255))
        img_rgb.paste(img, mask=img.split()[3])
        img = img_rgb
    img.save(destination_path)
    return destination_path


async def download_files(
    filepaths: List[str],
    destination_directory: str,
) -> List[str]:
    tasks = []
    timeout = 10.0
    transport = httpx.AsyncHTTPTransport(
        retries=3,
    )
    async with httpx.AsyncClient(
        timeout=timeout,
        transport=transport,
    ) as client:
        for f in filepaths:
            basename = os.path.basename(f)
            d = os.path.join(destination_directory, basename)
            tasks.append(download_file(client, f, d))
        destination_paths = await asyncio.gather(*tasks)
    return destination_paths


def download_dataset(
    bucket: str,
    filepaths: List[str],
    destination_directory: str,
) -> List[str]:
    os.makedirs(destination_directory, exist_ok=True)
    urls = [os.path.join("https://storage.googleapis.com/", bucket, f) for f in filepaths]
    loop = asyncio.get_event_loop()
    destination_paths = loop.run_until_complete(
        download_files(
            filepaths=urls,
            destination_directory=destination_directory,
        )
    )
    return destination_paths
