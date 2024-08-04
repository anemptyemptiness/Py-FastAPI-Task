from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from pydantic import TypeAdapter

from app.auth.helpers import get_current_user
from app.exceptions.todo_list_exceptions import (
    NoOneModifiedTask,
    NotEnoughRightsException,
    TaskNotFound
)
from app.exceptions.user_exceptions import UserNotFound
from app.todo_list.dao import TaskDAO
from app.todo_list.schemas import TaskSchema, TaskUpdateSchema
from app.users.dao import UserDAO
from app.users.schemas import UserSchema

router = APIRouter(
    prefix="/task",
    tags=["Взаимодействие с TODO-листом"],
)


@router.get("/tasks/", response_model=list[TaskSchema], status_code=200)
async def get_tasks(user: UserSchema = Depends(get_current_user)):
    tasks = await TaskDAO.get_tasks(user_id=user.user_id)

    if not tasks:
        raise TaskNotFound

    return [TypeAdapter(TaskSchema).dump_python(task) for task in tasks]


@router.get("/{task_id}/", response_model=TaskSchema, status_code=200)
async def get_task(
        task_id: Annotated[int, Path()],
        user: UserSchema = Depends(get_current_user),
):
    task = await TaskDAO.get_task(
        user_id=user.user_id,
        task_id=task_id,
    )
    if not task:
        raise TaskNotFound

    return TypeAdapter(TaskSchema).dump_python(task)


@router.post("", response_model=TaskSchema, status_code=201)
async def create_task(
    description: Annotated[str, Query()],
    user: UserSchema = Depends(get_current_user),
):
    created_task = await TaskDAO.create_task(
        user_id=user.user_id,
        description=description,
    )
    return TypeAdapter(TaskSchema).dump_python(created_task)


@router.patch("/{task_id}/", response_model=TaskSchema, status_code=200)
async def update_task(
        task_id: Annotated[int, Path()],
        description: Annotated[str, Query()] = None,
        status: Annotated[str, Query()] = None,
        user: UserSchema = Depends(get_current_user),
):
    user_task = await TaskDAO.get_task(
        user_id=user.user_id,
        task_id=task_id,
    )

    if not user_task:
        raise TaskNotFound
    if not description and not status:
        raise NoOneModifiedTask
    if user_task.owner != user.user_id:
        can_update = await TaskDAO.check_for_rights(
            task_id=task_id,
            user_id=user.user_id,
        )
        if not can_update:
            raise NotEnoughRightsException

    updated_task = await TaskDAO.update_task(
        task_id=task_id,
        task_update=TaskUpdateSchema(
            description=description,
            status=status,
        )
    )
    return TypeAdapter(TaskSchema).dump_python(updated_task)


@router.delete("/{task_id}/", response_model=dict, status_code=200)
async def delete_task(
        task_id: Annotated[int, Path()],
        user: UserSchema = Depends(get_current_user),
):
    user_task = await TaskDAO.get_task(
        user_id=user.user_id,
        task_id=task_id,
    )

    if not user_task:
        raise TaskNotFound
    if user_task.owner != user.user_id:
        raise NotEnoughRightsException

    await TaskDAO.delete_task(task_id=task_id)

    return {"message": "Task successfully deleted"}


@router.patch("/rights/{task_id}/", response_model=dict, status_code=200)
async def update_task_rights(
        task_id: Annotated[int, Path()],
        rights_to: Annotated[str, Query()],
        can_read: Annotated[bool, Query()] = True,
        can_update: Annotated[bool, Query()] = True,
        user: UserSchema = Depends(get_current_user),
):
    user_task = await TaskDAO.get_task(
        user_id=user.user_id,
        task_id=task_id,
    )

    if not user_task:
        raise TaskNotFound

    another_user = await UserDAO.get_user(user_login=rights_to)

    if not another_user:
        raise UserNotFound
    if user_task.owner != user.user_id:
        raise NotEnoughRightsException

    rights = {
        rights_to: {
            "can_read": can_read,
            "can_update": can_update,
        }
    }

    await TaskDAO.set_rights_by_task(
        owner_id=user.user_id,
        task_id=task_id,
        rights=rights,
        slave_login=rights_to,
    )

    return {
        "message": f"You have changed the rights for user {rights_to}"
    }
