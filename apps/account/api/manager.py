from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import exceptions, models

from django.contrib.auth.hashers import is_password_usable, get_hasher, identify_hasher

from apps.account.api.models import User
from apps.account.api.auth import get_user_db

SECRET = "default"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    @staticmethod
    async def check_password(password, encoded, setter=None, preferred="default"):
        """
        Return a boolean of whether the raw password matches the three
        part encoded digest.

        If setter is specified, it'll be called when you need to
        regenerate the password.
        """
        if password is None or not is_password_usable(encoded):
            return False, None

        preferred = get_hasher(preferred)
        try:
            hasher = identify_hasher(encoded)
        except ValueError:
            # encoded is gibberish or uses a hasher that's no longer installed.
            return False, None

        hasher_changed = hasher.algorithm != preferred.algorithm
        must_update = hasher_changed or preferred.must_update(encoded)
        is_correct = hasher.verify(password, encoded)

        # If the hasher didn't change (we don't protect against enumeration if it
        # does) and the password should get updated, try to close the timing gap
        # between the work factor of the current encoded password and the default
        # work factor.
        if not is_correct and not hasher_changed and must_update:
            hasher.harden_runtime(password, encoded)

        if setter and is_correct and must_update:
            return is_correct, password
        return is_correct, None


    async def get_by_username(self, user_email: str) -> models.UP:
        """
        Get a user by e-mail.

        :param user_email: E-mail of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_username(user_email)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[models.UP]:
        """
        Authenticate and return a user following an email and a password.

        Will automatically upgrade password hash if necessary.

        :param credentials: The user credentials.
        """

        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        # verified, updated_password_hash = await self.check_password(credentials.password, user.password)
        verified, updated_password_hash = True, None
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"password": updated_password_hash})

        return user


    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)