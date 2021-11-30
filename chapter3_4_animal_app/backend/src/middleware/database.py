import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__postgres_username = os.getenv("POSTGRES_USER")
__postgres_password = os.getenv("POSTGRES_PASSWORD")
__postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
__postgres_db = os.getenv("POSTGRES_DB")
__postgres_server = os.getenv("POSTGRES_SERVER")

__sql_alchemy_database_url = f"postgresql://{__postgres_username}:{__postgres_password}@{__postgres_server}:{__postgres_port}/{__postgres_db}?client_encoding=utf8"


engine = create_engine(
    __sql_alchemy_database_url,
    encoding="utf-8",
    pool_recycle=3600,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_session():
    db = SessionLocal()
    try:
        yield db
    except:
        db.rollback()
    finally:
        db.close()


Base = declarative_base()
