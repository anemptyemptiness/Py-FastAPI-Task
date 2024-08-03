from pydantic import BaseModel


class TaskSchema(BaseModel):
    task_id: int
    description: str
    owner: int
    status: str
    slaves: list[int]
    rights: dict[str, dict[str, bool]]


class TaskUpdateSchema(TaskSchema):
    task_id: int | None = None
    owner: int | None = None
    description: str | None = None
    status: str | None = None
    slaves: list[int] | None = None
    rights: dict[str, dict[str, bool]] | None = None
