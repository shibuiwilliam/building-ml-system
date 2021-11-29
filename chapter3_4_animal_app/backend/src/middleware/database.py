import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


class DatabaseClient(object):
    def __init__(self):
        self.__postgres_username = os.getenv("POSTGRES_USER")
        self.__postgres_password = os.getenv("POSTGRES_PASSWORD")
        self.__postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
        self.__postgres_db = os.getenv("POSTGRES_DB")
        self.__postgres_server = os.getenv("POSTGRES_SERVER")

        self.__sql_alchemy_database_url = f"postgresql://{self.__postgres_username}:{self.__postgres_password}@{self.__postgres_server}:{self.__postgres_port}/{self.__postgres_db}?client_encoding=utf8"

        self.__engine = create_engine(
            self.__sql_alchemy_database_url,
            encoding="utf-8",
            pool_recycle=3600,
            echo=False,
        )

    def create_session(self) -> Session:
        return sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.__engine,
        )


Base = declarative_base()
