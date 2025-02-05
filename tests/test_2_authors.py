from httpx import AsyncClient

from .test_1_users import get_admin_token, get_headers, get_reader_token


async def test_create_authors(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.post(
        "/authors/",
        headers=get_headers(reader_token),
        json={"name": "Пушкин", "biography": "", "birth_date": "1799-01-06"},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"

    response = await ac.post(
        "/authors/",
        headers=get_headers(admin_token),
        json={"name": "Пушкин", "biography": "", "birth_date": "1799-01-06"},
    )
    assert response.status_code == 201

    response = await ac.post(
        "/authors/",
        headers=get_headers(admin_token),
        json={
            "name": "Толстой Л.Н.",
            "biography": "",
            "birth_date": "1828-09-09",
        },
    )
    assert response.status_code == 201

    response = await ac.post(
        "/authors/",
        headers=get_headers(admin_token),
        json={"name": "Тургенев", "biography": "", "birth_date": "1811-11-09"},
    )
    assert response.status_code == 201


async def test_get_authors_list(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.get("/authors/", headers=get_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = await ac.get("/authors/", headers=get_headers(reader_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_author(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.get("/authors/1/", headers=get_headers(admin_token))
    assert response.status_code == 200

    response = await ac.get("/authors/1/", headers=get_headers(reader_token))
    assert response.status_code == 200


async def test_update_author(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.put(
        "/authors/1/",
        headers=get_headers(reader_token),
        json={"name": "Пушкин А.С."},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"

    response = await ac.put(
        "/authors/1/",
        headers=get_headers(admin_token),
        json={
            "name": "Пушкин А.С.",
            "biography": "Текст",
            "birth_date": "1799-06-06",
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Пушкин А.С."
    assert response.json()["biography"] == "Текст"
    assert response.json()["birth_date"] == "1799-06-06"


async def test_delete_author(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.delete(
        "/authors/3/", headers=get_headers(reader_token)
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"

    response = await ac.delete("/authors/3/", headers=get_headers(admin_token))
    assert response.status_code == 204
