from typing import AsyncGenerator, Generator, Union, Any

from sqlalchemy import MetaData, Table
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import NullPool

import asyncio

from conf import settings


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session

# DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
# Base = declarative_base()
#
#
# engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
# async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
#
# metadata = MetaData()
#
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
# from psycopg2cffi import compat
#
# compat.register()


DATABASE_URL = f"postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
Base = declarative_base()


engine = create_engine(DATABASE_URL, poolclass=NullPool)
session_factory = sessionmaker(engine, expire_on_commit=False)

metadata = MetaData()

def get_async_session() -> scoped_session[Union[Session, Any]]:
    return scoped_session(session_factory)
