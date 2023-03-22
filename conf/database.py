from typing import Union, Any

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, Session, scoped_session

from conf import settings


DATABASE_URL = f"postgresql+pg8000://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
Base = declarative_base()


engine = create_engine(DATABASE_URL, poolclass=NullPool)
session_factory = sessionmaker(engine, expire_on_commit=False)

metadata = MetaData()

def get_async_session() -> scoped_session[Union[Session, Any]]:
    return scoped_session(session_factory)