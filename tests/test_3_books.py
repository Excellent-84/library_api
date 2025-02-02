from httpx import AsyncClient

from .test_1_users import get_admin_token, get_headers, get_reader_token


async def test_create_book(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.post(
        "/books/",
        headers=get_headers(reader_token),
        json={
            "title": "Борис Годунов",
            "publication_date": "1833-01-01",
            "genre": "Поэзия",
            "available_copies": 5,
            "author_ids": [1]
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"

    response = await ac.post(
        "/books/",
        headers=get_headers(admin_token),
        json={
            "title": "Онегин",
            "publication_date": "1833-05-26",
            "genre": "Драма",
            "available_copies": 5,
            "author_ids": [1, 2]
        }
    )
    assert response.status_code == 201

    response = await ac.post(
        "/books/",
        headers=get_headers(admin_token),
        json={
            "title": "Борис Годунов",
            "publication_date": "1831-03-01",
            "genre": "Поэзия",
            "available_copies": 5,
            "author_ids": [1]
        }
    )
    assert response.status_code == 201


async def test_get_books_list(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.get("/books/", headers=get_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = await ac.get("/books/", headers=get_headers(reader_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_book(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.get("/books/1", headers=get_headers(admin_token))
    assert response.status_code == 200

    response = await ac.get("/books/1", headers=get_headers(reader_token))
    assert response.status_code == 200


async def test_update_book(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.put(
        "/books/1",
        headers=get_headers(reader_token),
        json={
            "title": "Евгений Онегин",
            "description": "Текст",
            "publication_date": "1833-01-01",
            "genre": "Поэзия",
            "available_copies": 1,
            "author_ids": [1]
        }
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"

    response = await ac.put(
        "/books/1",
        headers=get_headers(admin_token),
        json={
            "title": "Евгений Онегин",
            "description": "Текст",
            "publication_date": "1833-01-01",
            "genre": "Поэзия",
            "available_copies": 1,
            "author_ids": [1]
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Евгений Онегин"
    assert response.json()["description"] == "Текст"
    assert response.json()["publication_date"] == "1833-01-01"
    assert response.json()["genre"] == "Поэзия"
    assert response.json()["available_copies"] == 1
    assert response.json()["authors"] == ["Пушкин А.С."]


async def test_delete_book(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.delete("/books/2", headers=get_headers(reader_token))
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"

    response = await ac.delete("/books/2", headers=get_headers(admin_token))
    assert response.status_code == 204
