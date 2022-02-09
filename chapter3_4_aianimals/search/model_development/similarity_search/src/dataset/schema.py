from typing import List

from pydantic import BaseModel


class ImageShape(BaseModel):
    height: int = 224
    width: int = 224
    depth: int = 3
    color: str = "RGB"
