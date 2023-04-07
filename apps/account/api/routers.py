from random import shuffle

from fastapi_users import FastAPIUsers

from .models import User
from .auth import auth_backend
from .manager import get_user_manager
from .schemas import OAuth2PasswordRequestForm

from typing import Tuple

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from fastapi_users import models
from fastapi_users.authentication import AuthenticationBackend, Authenticator, Strategy
from fastapi_users.manager import BaseUserManager, UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel


router = APIRouter()

class CustomFastAPIUsers(FastAPIUsers[models.UP, models.ID]):
    def get_auth_router(
            self, backend: AuthenticationBackend, requires_verification: bool = False
    ) -> APIRouter:

        return get_auth_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )

async def insertion_sort(alist: list):
    for i in range(1, len(alist)):
        temp = alist[i]
        j = i - 1
        while j >= 0 and temp < alist[j]:
            alist[j + 1] = alist[j]
            j = j - 1
        alist[j + 1] = temp


fastapi_users = CustomFastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

IsAuthenticated = fastapi_users.current_user(active=True)

@router.get('/test1/')
async def get_user_test(user: User = Depends(IsAuthenticated)):
    random_list_of_nums = list(range(0, 1_000))
    shuffle(random_list_of_nums)
    await insertion_sort(random_list_of_nums)
    print(user)

    return {
        "status": "success",
        "data": random_list_of_nums,
        "details": None
    }


def get_auth_router(
    backend: AuthenticationBackend,
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    authenticator: Authenticator,
    requires_verification: bool = False,
) -> APIRouter:
    """Generate a router with login/logout routes for an authentication backend."""
    router = APIRouter()
    get_current_user_token = authenticator.current_user_token(
        active=True, verified=requires_verification
    )

    login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Bad credentials or the user is inactive.",
                            "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post(
        "/login",
        name=f"auth:{backend.name}.login",
        responses=login_responses,
    )
    async def login(
        request: Request,
        response: Response,
        credentials: OAuth2PasswordRequestForm = Depends(),
        user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
        strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        login_return = await backend.login(strategy, user, response)
        await user_manager.on_after_login(user, request)
        return login_return

    logout_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/logout", name=f"auth:{backend.name}.logout", responses=logout_responses
    )
    async def logout(
        response: Response,
        user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
        strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
    ):
        user, token = user_token
        return await backend.logout(strategy, user, token, response)

    return router