from fastapi import HTTPException, status


class TaskNotFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Task not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NoOneModifiedTask(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Select at least one field to modify"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class NotEnoughRightsException(HTTPException):
    status = status.HTTP_403_FORBIDDEN
    detail = "Not enough rights to this task"

    def __init__(self):
        super().__init__(status_code=self.status, detail=self.detail)