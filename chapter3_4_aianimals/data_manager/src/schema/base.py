from sqlalchemy.ext.declarative import declarative_base
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)

Base = declarative_base()
