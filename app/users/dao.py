from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.database import async_session
from app.users.models import User


class UserDAO:
    @classmethod
    async def get_user(
            cls,
            user_login: str,
    ):
        async with async_session() as session:
            query = (
                select(User)
                .where(User.login == user_login)
            )

            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def add_user(
            cls,
            login: str,
            password: bytes,
    ):
        async with async_session() as session:
            stmt = (
                insert(User)
                .values(
                    login=login,
                    password=password,
                )
            )

            await session.execute(stmt)
            await session.commit()