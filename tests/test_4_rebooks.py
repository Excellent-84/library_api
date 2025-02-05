from httpx import AsyncClient

from .test_1_users import get_admin_token, get_headers, get_reader_token


async def test_borrow_book(ac: AsyncClient):
    reader_token = await get_reader_token(ac)
    admin_token = await get_admin_token(ac)

    response = await ac.post(
        "/rebooks/",
        headers=get_headers(reader_token),
        json={"book_id": 1}
    )
    assert response.status_code == 201
    assert response.json()["user_id"] == 2
    assert response.json()["book_id"] == 1
    assert "borrowed_at" in response.json()
    assert "due_date" in response.json()
    assert response.json()["returned_at"] is None

    response = await ac.post(
        "/rebooks/",
        headers=get_headers(admin_token),
        json={"book_id": 1}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "No copies available"

    response = await ac.get("/books/1", headers=get_headers(reader_token))
    assert response.json()["available_copies"] == 0


async def test_return_book(ac: AsyncClient):
    reader_token = await get_reader_token(ac)

    response = await ac.post(
        "/rebooks/return",
        headers=get_headers(reader_token),
        json={"book_id": 1}
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == 2
    assert response.json()["book_id"] == 1
    assert "borrowed_at" in response.json()
    assert "due_date" in response.json()
    assert response.json()["returned_at"] is not None

    response = await ac.get("/books/1", headers=get_headers(reader_token))
    assert response.json()["available_copies"] == 1


async def test_get_rebook(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.get("/rebooks/1", headers=get_headers(admin_token))
    assert response.status_code == 200

    response = await ac.get("/rebooks/1", headers=get_headers(reader_token))
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"


async def test_get_rebooks_list(ac: AsyncClient):
    admin_token = await get_admin_token(ac)
    reader_token = await get_reader_token(ac)

    response = await ac.get("/rebooks/", headers=get_headers(admin_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = await ac.get("/rebooks/", headers=get_headers(reader_token))
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"
