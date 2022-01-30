import asyncio
import os
from io import BytesIO
from typing import List

import httpx
from PIL import Image


async def download_file(
    client: httpx.AsyncClient,
    source_path: str,
    destination_path: str,
) -> str:
    res = await client.get(source_path)
    if res.status_code != 200:
        raise Exception(f"failed to download {source_path}")
    img = Image.open(BytesIO(res.content))
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
