from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from src.configurations import Configurations


engine = create_engine(
    Configurations.sql_alchemy_database_url,
    encoding="utf-8",
    pool_recycle=3600,
    echo=False,
)

Base = declarative_base()

session_factory = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
Session = scoped_session(session_factory=session_factory)


def get_db(func):
    def _get_db(*args, **kwargs):
        db = Session()
        try:
            func(*args, **kwargs)
            db.commit()
        except:
            db.rollback()
            raise
        finally:
            Session.remove()

    return _get_db
