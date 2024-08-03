from jwt import InvalidTokenError

from fastapi import Depends, Form, Request

from app.exceptions.auth_exceptions import (
    UnAuthedUserException,
    UserNotFoundException,
    InvalidTokenException,
)
from app.users.dao import UserDAO
from app.users.schemas import UserSchema
import app.auth.utils as auth_utils


def get_current_token_payload(
        request: Request,
) -> dict:
    token = request.cookies.get("access_token")
    try:
        payload = auth_utils.decode_jwt(token=token)
        return payload
    except InvalidTokenError:
        raise InvalidTokenException


async def get_current_user(
        payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub", None)

    if not (user := await UserDAO.get_user(username)):
        raise UserNotFoundException

    return UserSchema(
        login=user.login,
        user_id=user.user_id,
        password=user.password,
    )


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):

    if not (user := await UserDAO.get_user(username)):
        raise UnAuthedUserException

    if not auth_utils.validate_password(
            password=password,
            hashed_password=user.password,
    ):
        raise UnAuthedUserException

    return user