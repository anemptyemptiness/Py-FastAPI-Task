from sqlalchemy import select, update, delete, and_, func, union, any_, exists
from sqlalchemy.dialects.postgresql import insert

from app.database import async_session
from app.todo_list.models import Task
from app.users.models import User
from app.todo_list.schemas import TaskUpdateSchema


class TaskDAO:
    @classmethod
    async def get_tasks(
            cls,
            user_id: int,
    ):
        async with async_session() as session:
            task_ids = (
                union(
                    select(Task.task_id)
                    .where(Task.owner == user_id),
                    select(Task.task_id)
                    .where(user_id == any_(Task.slaves))
                    .group_by(Task.task_id)
                )
            ).cte("task_ids")

            query = (
                select(Task)
                .where(Task.task_id.in_(select(task_ids.c.task_id)))
            )

            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_task(
            cls,
            user_id: int,
            task_id: int,
    ):
        async with async_session() as session:
            task_ids = (
                union(
                    select(Task.task_id)
                    .where(Task.owner == user_id),
                    select(Task.task_id)
                    .where(user_id == any_(Task.slaves))
                    .group_by(Task.task_id)
                )
            ).cte("task_ids")

            query = (
                select(Task)
                .where(
                    Task.task_id == (select(task_ids.c.task_id).where(task_ids.c.task_id == task_id)).scalar_subquery()
                )
            )

            result = await session.execute(query)
            return result.scalar()

    @classmethod
    async def create_task(
            cls,
            user_id: int,
            description: str,
    ):
        async with async_session() as session:
            stmt = (
                insert(Task)
                .values(
                    description=description,
                    owner=user_id,
                )
                .returning(Task)
            )

            created_task = await session.execute(stmt)
            await session.commit()

            return created_task.scalar()

    @classmethod
    async def update_task(
            cls,
            task_id: int,
            task_update: TaskUpdateSchema,
    ):
        async with async_session() as session:
            stmt = (
                update(Task)
                .values(**task_update.model_dump(exclude_none=True))
                .where(Task.task_id == task_id)
                .returning(Task)
            )

            updated_task = await session.execute(stmt)
            await session.commit()

            return updated_task.scalar()

    @classmethod
    async def delete_task(
            cls,
            task_id: int,
    ):
        async with async_session() as session:
            stmt = (
                delete(Task)
                .where(Task.task_id == task_id)
            )

            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def set_rights_by_task(
            cls,
            owner_id: int,
            task_id: int,
            rights: dict,
            slave_login: str,
    ):
        async with async_session() as session:
            slave_id = select(User.user_id).where(User.login == slave_login).cte("slave_id")

            is_slave_in_array_query = (
                select(slave_id)
                .where(slave_id.c.user_id == any_(Task.slaves))
            )
            is_slave_in_array = (await session.execute(is_slave_in_array_query)).scalar()

            stmt = (
                update(Task)
                .values(
                    rights=rights,
                    slaves=func.array_append(
                        Task.slaves,
                        select(User.user_id).where(User.login == slave_login).scalar_subquery()
                    )
                    if not is_slave_in_array
                    else Task.slaves,
                )
                .where(
                    and_(
                        Task.owner == owner_id,
                        Task.task_id == task_id
                    )
                )
                .returning(Task)
            )

            updated_task = await session.execute(stmt)
            await session.commit()

            return updated_task.scalar()

    @classmethod
    async def check_for_rights(
            cls,
            task_id: int,
            user_id: int,
    ):
        async with async_session() as session:
            query = (
                select(Task)
                .where(Task.task_id == task_id)
            )

            task = (await session.execute(query)).scalar()

            if task.owner != user_id:
                query = (
                    select(User.login)
                    .where(User.user_id == user_id)
                )

                user_login = (await session.execute(query)).scalar()

                if not task.rights.get(user_login, None):
                    return False
                else:
                    if not task.rights.get(user_login).get("can_update", None):
                        return False

            return True
