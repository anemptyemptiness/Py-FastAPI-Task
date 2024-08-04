from sqlalchemy import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    password: Mapped[bytes] = mapped_column(LargeBinary)
