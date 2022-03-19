import asyncio
import os
from io import BytesIO
from typing import List, Optional

import httpx
from PIL import Image
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


async def download_file(
    client: httpx.AsyncClient,
    source_path: str,
    destination_path: str,
) -> Optional[str]:
    logger.info(f"download {source_path}: {destination_path}")
    if os.path.exists(destination_path):
        return destination_path
    try:
        res = await client.get(source_path)
    except httpx.PoolTimeout as e:
        logger.error(f"timeout {e}: failed to download data: {source_path}")
        return None
    if res.status_code != 200:
        logger.error(f"status code {res.status_code}: failed to download data: {source_path}")
        return None
    img = Image.open(BytesIO(res.content))
    if img.mode == "RGB":
        img = img
    elif img.mode == "RGBA":
        img_rgb = Image.new("RGB", (img.height, img.width), (255, 255, 255))
        img_rgb.paste(img, mask=img.split()[3])
        img = img_rgb
    else:
        return None
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
    filepaths: List[str],
    destination_directory: str,
) -> List[str]:
    logger.info("start downloading image")
    os.makedirs(destination_directory, exist_ok=True)
    _filepaths = []
    _f = []
    for i, f in enumerate(filepaths):
        _f.append(f)
        if i != 0 and i % 500 == 0:
            _filepaths.append(_f)
            _f = []
    _filepaths.append(_f)
    destination_paths = []
    for fs in _filepaths:
        loop = asyncio.get_event_loop()
        _destination_paths = loop.run_until_complete(
            download_files(
                filepaths=fs,
                destination_directory=destination_directory,
            )
        )
        destination_paths.extend(_destination_paths)
    logger.info("done downloading image")
    destination_paths = [f for f in destination_paths if f is not None]
    return destination_paths
