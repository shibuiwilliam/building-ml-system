import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

postgres_username = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_port = int(os.getenv("POSTGRES_PORT", 5432))
postgres_db = os.getenv("POSTGRES_DB")
postgres_server = os.getenv("POSTGRES_SERVER")

sql_alchemy_database_url = f"postgresql://{postgres_username}:{postgres_password}@{postgres_server}:{postgres_port}/{postgres_db}?client_encoding=utf8"


engine = create_engine(
    sql_alchemy_database_url,
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
    finally:
        db.close()


Base = declarative_base()
