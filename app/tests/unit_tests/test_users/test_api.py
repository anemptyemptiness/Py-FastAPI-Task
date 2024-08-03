from httpx import AsyncClient
import pytest


@pytest.mark.parametrize("login, password, status_code", [
    ("anempty", "qwerty", 201),
    ("", "", 422),
    ("", "qwerty", 422),
    ("anempty", "", 422),
])
async def test_register_user(login, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register/", json={
        "username": login,
        "password": password,
    })
    assert response.status_code == status_code
