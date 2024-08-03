from datetime import datetime, timedelta

import bcrypt
import jwt

from app.config import settings, settings_auth


def encode_jwt(
        payload: dict,
        key: str = settings_auth.private_key_path.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings_auth.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        exp=expire,
        iat=now,
    )

    encoded = jwt.encode(
        payload=to_encode,
        key=key,
        algorithm=algorithm,
    )

    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings_auth.public_key_path.read_text(),
        algorithm: str = settings.ALGORITHM,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm]
    )

    return decoded


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()

    return bcrypt.hashpw(password=password_bytes, salt=salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )