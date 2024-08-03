import json

import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("login, password", [
    ("anempty", "qwerty"),
])
async def test_register_user_and_create_task_and_get_tasks(login, password, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": login,
        "password": password,
    }, follow_redirects=True)
    assert response.status_code == 201

    response = await ac.get("/task/tasks", follow_redirects=True)
    assert response.status_code == 404

    response = await ac.post("/task/", params={
        "description": "desc_777",
    }, follow_redirects=True)
    assert response.status_code == 201

    response = await ac.get("/task/tasks", follow_redirects=True)
    tasks = json.loads(response.content)
    first_task = tasks[0]
    assert first_task.get("description") == "desc_777"


@pytest.mark.parametrize("login, password", [
    ("anempty", "qwerty"),
])
async def test_register_user_and_create_task_and_update_task(login, password, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": login,
        "password": password,
    }, follow_redirects=True)
    assert response.status_code == 201

    response = await ac.post("/task/", params={
        "description": "desc_777",
    }, follow_redirects=True)
    assert response.status_code == 201

    task_id = json.loads(response.content.decode()).get("task_id")

    response = await ac.patch(f"/task/{task_id}", params={
        "description": "updated description"
    }, follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize("login, password", [
    ("anempty", "qwerty"),
])
async def test_register_user_and_create_task_and_delete_task(login, password, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "username": login,
        "password": password,
    }, follow_redirects=True)
    assert response.status_code == 201

    response = await ac.post("/task/", params={
        "description": "desc_777",
    }, follow_redirects=True)
    assert response.status_code == 201

    task_id = json.loads(response.content.decode()).get("task_id")

    response = await ac.delete(f"/task/{task_id}", follow_redirects=True)
    assert response.status_code == 200
