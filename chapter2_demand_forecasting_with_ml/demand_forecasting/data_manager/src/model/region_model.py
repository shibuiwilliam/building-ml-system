from pydantic import Extra
from src.model.abstract_model import AbstractModel


class Region(AbstractModel):
    id: str
    name: str

    class Config:
        extra = Extra.forbid
