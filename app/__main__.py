from fastapi import FastAPI

from app.todo_list.router import router as todo_list_router
from app.auth.router import router as auth_router

app = FastAPI()
app.include_router(todo_list_router)
app.include_router(auth_router)
