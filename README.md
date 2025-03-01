## API для Управления Библиотекой

<br>

<div style="display: flex; flex-wrap: wrap;">
  <img src="https://www.python.org/static/community_logos/python-logo.png" alt="Python" width="84"/>
  <img src="https://img.shields.io/badge/FastAPI-FFFFFF?style=for-the-badge&logo=fastapi logoColor=009688"/>
  <img src="https://img.shields.io/badge/sqlalchemy-FFFFFF?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/>
  <img src="https://img.shields.io/badge/pydantic-FFFFFF?style=for-the-badge&logo=pydantic&logoColor=E92063"/>
  <img src="https://img.shields.io/badge/alembic-FFFFFF?style=for-the-badge&logo=alembic&logoColor=8212"/>
  <img src="https://img.shields.io/badge/PostgreSQL-FFFFFF?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/>
  <img src="https://img.shields.io/badge/JWT-FFFFFF?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=black"/>
  <img src="https://img.shields.io/badge/pytest-FFFFFF?style=for-the-badge&logo=pytest&logoColor=0A9EDC"/>
  <img src="https://img.shields.io/badge/Docker-FFFFFF?style=for-the-badge&logo=Docker&logoColor=2496ED"/>
</div>

<br>

<details>
<summary><strong>Описание проекта</strong></summary>
<br><br>
RESTful API для управления библиотечным каталогом. Система позволяет управлять информацией о книгах, авторах, читателях и выдачей книг.
<br>

 - Регистрация и Аутентификация пользователей с использованием JWT токенов по email. Пользователи разделены на роли: администратор и читатель. Первому зарегистрированному пользователю присваивается роль администратора, всем последующим - читатель. Администратор может изменять роли пользователей. Администратор может управлять всеми ресурсами, читатель — только просмотр и взаимодействие с книгами.

 - Управление книгами. CRUD операции для книг.

 - Управление авторами. CRUD операции для авторов.

 - Управление читателями. Администратор может просматривать список читателей. Читатели могут обновлять свою информацию.

 - Выдача и возврат книг. Возможность выдачи книги читателю. Ограничение количества выдаваемых книг на одного читателя до 5. Фиксация даты выдачи и предполагаемой даты возврата. Обработка возврата книг и обновление количества доступных экземпляров.

 - Дополнительно:
   - Пагинация и фильтрация для списков книг, авторов и выданных книг.
   - Валидация входящих данных с использованием Pydantic.
   - Обработка ошибок с соответствующими HTTP статусами.
   - Логирование основных событий.
   - Alembic для управления миграциями базы данных.
   - Юнит-тесты для основных эндпоинтов.
   - Документация ReDoc, Swagger.
   - Развертывание проекта с помощью Docker.

</details>

<details>
<summary><strong>Как запустить проект</strong></summary>

##### Клонировать репозиторий и перейти в него в командной строке:

```bash
$ git clone https://github.com/Excellent-84/library_api.git
$ cd library_api
```

##### Создать файл .env и указать необходимые токены по примеру .env.example:

```bash
$ touch .env
```

##### Собрать и запустить контейнеры с помощью Docker:

```bash
$ docker compose up -d
```

##### При необходимости проверить логи запущенного контейнера:

```bash
$ docker logs library_api
```

##### Проект будет доступен по адресу:

```bash
http://localhost:8000
```

##### Тестирование. Запуск тестов pytest внутри контейнера:

```bash
$ docker exec -it library_api pytest
```

</details>

<details>
<summary><strong>Примеры запросов к API с помощью Postman</strong></summary>

##### Регистрация пользователя в базе данных:

Метод POST к эндпоинту   http://localhost:8000/users/register/

Во вкладке Body выбрать raw. Указать данные в формате json.
Пример запроса:

```bash
{
  "email": "example@example.com",
  "username": "example_user",
  "password": "example_password"
}
```

Пример ответа:

```bash
{
  "email": "example@example.com",
  "id": 1,
  "username": "example_user",
  "is_active": true,
  "role": "reader"
}
```

##### Аутентификация пользователя:

Метод POST к эндпоинту   http://localhost:8000/users/login/

Во вкладке Body выбрать raw. Указать данные в формате json.
Срок действия токена 30 минут, после чего необходимо пройти повторную аутентификацию.
Пример запроса:

```bash
{
  "email": "example@example.com",
  "password": "example_password"
}
```

Пример ответа:

```bash
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...",
  "token_type": "bearer"
}
```

##### Получение списка доступных книг:

Метод GET к эндпоинту   http://localhost:8000/books/

Во вкладке Auth в поле Type выбрать Bearer Token.
В поле Token скопировать значение access_token, полученного при аутентификации.

Пример ответа:

```bash
[
  {
    "title": "Война и Мир",
    "description": "Роман, описывающий...",
    "publication_date": "1869-01-01",
    "genre": "Роман",
    "available_copies": 5,
    "id": 1,
    "authors": [
      "Лев Толстой"
    ]
  },
  ...
]
```

##### Получение книги по ID:

Метод GET к эндпоинту   http://localhost:8000/books/{book_id}/

Во вкладке Auth в поле Type выбрать Bearer Token.
В поле Token скопировать значение access_token, полученного при аутентификации.

Пример ответа:

```bash
{
  "title": "Война и Мир",
  "description": "Роман, описывающий...",
  "publication_date": "1869-01-01",
  "genre": "Роман",
  "available_copies": 5,
  "id": 1,
  "authors": [
    "Лев Толстой"
  ]
}
```

##### Выдача книги:

Метод POST к эндпоинту   http://localhost:8000/rebooks/

Во вкладке Auth в поле Type выбрать Bearer Token.
В поле Token скопировать значение access_token, полученного при аутентификации.
Во вкладке Body выбрать raw. Указать данные в формате json.
Пример запроса:

```bash
{
  "book_id": 1
}
```

Пример ответа:

```bash
{
  "book_id": 1,
  "id": 101,
  "borrowed_at": "2025-02-02T10:00:00",
  "due_date": "2025-02-16T10:00:00",
  "returned_at": "2025-02-14T15:00:00",
  "user_id": 42
}
```

##### Возврат книги:

Метод POST к эндпоинту   http://localhost:8000/rebooks/return/

Во вкладке Auth в поле Type выбрать Bearer Token.
В поле Token скопировать значение access_token, полученного при аутентификации.
Во вкладке Body выбрать raw. Указать данные в формате json.
Пример запроса:

```bash
{
  "book_id": 1
}
```

Пример ответа:

```bash
{
  "book_id": 1,
  "id": 101,
  "borrowed_at": "2025-02-02T10:00:00",
  "due_date": "2025-02-16T10:00:00",
  "returned_at": "2025-02-14T15:00:00",
  "user_id": 42
}
```

<br>

<strong>Подробную версию запросов можно посмотреть по адресу:</strong>
- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

</details>

<br>

<strong>Автор: [Горин Евгений](https://github.com/Excellent-84)</strong>