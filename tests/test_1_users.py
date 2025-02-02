from httpx import AsyncClient


async def register_user(
    ac: AsyncClient, email: str, password: str, username: str
):
    response = await ac.post(
        "/users/register",
        json={"email": email, "password": password, "username": username},
    )
    assert response.status_code == 201


async def login_user(ac: AsyncClient, email: str, password: str) -> str:
    response = await ac.post(
        "/users/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    return response.json()["access_token"]


def get_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


async def get_admin_token(ac: AsyncClient) -> str:
    return await login_user(ac, "admin@example.com", "adminpassword")


async def get_reader_token(ac: AsyncClient) -> str:
    return await login_user(ac, "reader@example.com", "readerpassword")


async def test_register(ac: AsyncClient):
    await register_user(ac, "admin@example.com", "adminpassword", "adminuser")


async def test_login(ac: AsyncClient):
    admin_token = await get_admin_token(ac)

    await register_user(
        ac, "reader@example.com", "readerpassword", "readeruser"
    )
    reader_token = await get_reader_token(ac)

    assert admin_token is not None
    assert reader_token is not None


async def test_get_users_list(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    response = await ac.get("/users/", headers=get_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    reader_token = await get_reader_token(ac)
    response = await ac.get("/users/", headers=get_headers(reader_token))
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"


async def test_get_user(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.get("/users/2", headers=get_headers(admin_token))
    assert response.status_code == 200

    response = await ac.get("/users/2", headers=get_headers(reader_token))
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"


async def test_get_me(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    response = await ac.get("/users/me", headers=get_headers(admin_token))
    assert response.status_code == 200
    assert response.json()["email"] == "admin@example.com"
    assert response.json()["role"] == "admin"

    reader_token = await get_reader_token(ac)
    response = await ac.get("/users/me", headers=get_headers(reader_token))
    assert response.status_code == 200
    assert response.json()["email"] == "reader@example.com"
    assert response.json()["role"] == "reader"


async def test_update_me(ac: AsyncClient):
    reader_token = await get_reader_token(ac)
    headers = get_headers(reader_token)

    response = await ac.put(
        "/users/me", headers=headers, json={"username": "updateduser"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

    response = await ac.put(
        "/users/me", headers=headers, json={"password": "newpassword"}
    )
    assert response.status_code == 200

    response = await ac.put(
        "/users/me",
        headers=headers,
        json={"password": "readerpassword", "username": "readeruser"},
    )
    assert response.status_code == 200


async def test_update_role(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    headers = get_headers(admin_token)

    response = await ac.put(
        "/users/2/role", headers=headers, json={"new_role": "admin"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Role updated to admin"

    response = await ac.put(
        "/users/2/role", headers=headers, json={"new_role": "reader"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Role updated to reader"

    reader_token = await get_reader_token(ac)
    response = await ac.put(
        "/users/2/role",
        headers=get_headers(reader_token),
        json={"new_role": "admin"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"
