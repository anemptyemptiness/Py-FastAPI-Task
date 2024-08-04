from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response

import app.auth.utils as auth_utils
from app.auth.helpers import validate_auth_user
from app.auth.schemas import TokenInfo
from app.exceptions.auth_exceptions import UserAlreadyRegisteredException
from app.users.dao import UserDAO
from app.users.schemas import UserSchema

router = APIRouter(
    tags=["Авторизация и Аутентификация"],
    prefix="/auth"
)


@router.post("/register/", response_model=TokenInfo, status_code=201)
async def register_user(
    response: Response,
    username: Annotated[str, Body(min_length=5)],
    password: Annotated[str, Body(min_length=5)],
):
    if await UserDAO.get_user(username):
        raise UserAlreadyRegisteredException

    hashed_password = auth_utils.hash_password(password=password)
    await UserDAO.add_user(
        login=username,
        password=hashed_password,
    )
    jwt_payload = {"sub": username}
    access_token = auth_utils.encode_jwt(payload=jwt_payload)
    response.set_cookie("access_token", access_token, httponly=True)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )


@router.post("/login/", response_model=TokenInfo)
async def login_user(
    response: Response,
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {"sub": user.login}
    access_token = auth_utils.encode_jwt(payload=jwt_payload)
    response.set_cookie("access_token", access_token, httponly=True)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )
