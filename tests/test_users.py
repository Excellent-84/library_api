from httpx import AsyncClient


async def test_register(ac: AsyncClient):
    response = await ac.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "username": "testuser",
        },
    )

    assert response.status_code == 201


async def test_login(ac: AsyncClient):
    response = await ac.post(
        "/users/login",
        json={"email": "test@example.com", "password": "testpassword"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"

    return response.json()["access_token"]


async def test_get_me(ac: AsyncClient):
    access_token = await test_login(ac)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await ac.get("/users/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


async def test_update_me(ac: AsyncClient):
    access_token = await test_login(ac)
    headers = {"Authorization": f"Bearer {access_token}"}

    response = await ac.put(
        "/users/me", headers=headers, json={"username": "updateduser"}
    )

    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

    response = await ac.put(
        "/users/me", headers=headers, json={"password": "newpassword"}
    )
    assert response.status_code == 200
