from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, INTEGER, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Task(Base):
    __tablename__ = "task"

    task_id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str]
    status: Mapped[str] = mapped_column(default="not complited")
    owner: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    slaves: Mapped[list[int]] = mapped_column(ARRAY(INTEGER), default={})
    rights: Mapped[dict[str, dict[str, bool]]] = mapped_column(JSON, default={})
