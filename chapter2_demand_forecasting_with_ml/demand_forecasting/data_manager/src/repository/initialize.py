from sqlalchemy import Column, Index

from sqlalchemy.engine import Engine
from src.middleware.logger import configure_logger
from src.repository import models
from src.repository.db import Base

logger = configure_logger(name=__name__)
