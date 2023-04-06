from fastapi import Depends
from sqlalchemy.orm import Session
from conf.database import get_async_session
from fastapi_users.db import SQLAlchemyUserDatabase

from typing import Optional
from fastapi_users.models import UP
from sqlalchemy import func, select
from sqlalchemy.sql import Select

from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend, BearerTransport

from .models import User

from conf import settings

class CustomSQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    session: Session

    async def _get_user(self, statement: Select) -> Optional[UP]:
        results = self.session.execute(statement)
        return results.unique().scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[UP]:
        statement = select(self.user_table).where(
            func.lower(self.user_table.username) == func.lower(username)
        )
        return await self._get_user(statement)


cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name='media_rinh')


async def get_user_db(session: Session = Depends(get_async_session)):
    yield CustomSQLAlchemyUserDatabase(session, User)


async def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRET_KEY, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)