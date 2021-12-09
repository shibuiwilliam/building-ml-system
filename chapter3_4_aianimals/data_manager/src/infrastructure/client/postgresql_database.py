import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database import AbstractDatabase
from src.middleware.logger import configure_logger

logger = configure_logger(__name__)


class PostgreSQLDatabase(AbstractDatabase):
    def __init__(self):
        super().__init__()

        self.__postgres_username = os.getenv("POSTGRES_USER")
        self.__postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.__postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.__postgres_db = os.getenv("POSTGRES_DB")
        self.__postgres_server = os.getenv("POSTGRES_SERVER")

        self.__sql_alchemy_database_url = f"postgresql://{self.__postgres_username}:{self.__postgres_password}@{self.__postgres_server}:{self.__postgres_port}/{self.__postgres_db}?client_encoding=utf8"

        self.engine: Engine = create_engine(
            self.__sql_alchemy_database_url,
            encoding="utf-8",
            pool_recycle=3600,
            echo=False,
        )

        self.session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    def get_session(self):
        db = self.session_local()
        try:
            yield db
        except:
            db.rollback()
        finally:
            db.close()
