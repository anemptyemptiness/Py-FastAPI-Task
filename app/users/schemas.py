from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    user_id: int
    password: bytes
