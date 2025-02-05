## API для Управления Библиотекой

### Описание проекта:

RESTful API для управления библиотечным каталогом. Система позволяет управлять информацией о книгах, авторах, читателях и выдачей книг.

 - Регистрация и Аутентификация пользователей с использованием JWT токенов по email. Пользователи разделены на роли: администратор и читатель. Первому зарегистрированному пользователю присваивается роль администратора, всем последующим - читатель. Администратор может изменять роли пользователей. Администратор может управлять всеми ресурсами, читатель — только просмотр и взаимодействие с книгами.

 - Управление книгами. CRUD операции для книг. Каждая книга имеет следующие поля:
     - ID
     - Название
     - Описание
     - Дата публикации
     - Автор(ы) (связь с таблицей авторов)
     - Жанр(ы)
     - Количество доступных экземпляров

 - Управление авторами. CRUD операции для авторов. Поля автора:
     - ID
     - Имя
     - Биография
     - Дата рождения

 - Управление читателями. Администратор может просматривать список читателей. Читатели могут обновлять свою информацию.

 - Выдача и возврат книг. Возможность выдачи книги читателю. Ограничение количества выдаваемых книг на одного читателя до 5. Фиксация даты выдачи и предполагаемой даты возврата. Обработка возврата книг и обновление количества доступных экземпляров.

 - Дополнительно:
   - Пагинация и фильтрация для списков книг, авторов и выданных книг.
   - Валидация входящих данных с использованием Pydantic.
   - Обработка ошибок с соответствующими HTTP статусами.
   - Логирование основных событий.
   - Alembic для управления миграциями базы данных.
   - Юнит-тесты для основных эндпоинтов.
   - Документация ReDoc, Swagger


### Стек технологий:
<img src="https://img.shields.io/badge/Python-FFFFFF?style=for-the-badge&logo=python&logoColor=3776AB"/><img src="https://img.shields.io/badge/FastAPI-FFFFFF?style=for-the-badge&logo=fastapi&logoColor=009688"/><img src="https://img.shields.io/badge/pydantic-FFFFFF?style=for-the-badge&logo=pydantic&logoColor=E92063"/><img src="https://img.shields.io/badge/PostgreSQL-FFFFFF?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/><img src="https://img.shields.io/badge/sqlalchemy-FFFFFF?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/><img src="https://img.shields.io/badge/alembic-FFFFFF?style=for-the-badge&logo=alembic&logoColor=8212"/><img src="https://img.shields.io/badge/JWT-FFFFFF?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=black"/><img src="https://img.shields.io/badge/pytest-FFFFFF?style=for-the-badge&logo=pytest&logoColor=0A9EDC"/>


### Как запустить проект:

##### Клонировать репозиторий и перейти в него в командной строке:

```bash
$ git clone https://github.com/Excellent-84/library_api.git
$ cd library_api
```

##### Cоздать и активировать виртуальное окружение:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip
```

##### Установить зависимости из файла requirements.txt:

```bash
$ pip install -r requirements.txt
```

##### Создать файл .env и указать необходимые токены по примеру .env.example:

```bash
$ touch .env
```

##### Создать базу данных в PostgreSQL через pgAdmin или командную строку:

```bash
$ psql -U <DB_USER>
$ CREATE DATABASE <DB_NAME>;
```

##### При необходимости выполнить и применить миграции:

```bash
$ alembic revision --autogenerate -m "<ваш комментарий>"
$ alembic upgrade head
```

##### Запустить проект:

```bash
$ python main.py
```

##### Тестирование. Перед запуском тестирования нужно создать тестовую базу данных
##### в PostgreSQL, например test_db, в файле .test.env  необходимо указать
##### тестовые данные, отличные от файла .env:

```bash
$ pytest
```

### Примеры запросов к API с помощью Postman:

##### Регистрация пользователя в базе данных:

Метод POST к эндпоинту   http://127.0.0.1:8000/users/register/

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

Метод POST к эндпоинту   http://127.0.0.1:8000/users/login/

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

Метод GET к эндпоинту   http://127.0.0.1:8000/books/

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

Метод GET к эндпоинту   http://127.0.0.1:8000/books/{book_id}/

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

Метод POST к эндпоинту   http://127.0.0.1:8000/rebooks/

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

Метод POST к эндпоинту   http://127.0.0.1:8000/rebooks/return/

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

##### Подробную версию запросов можно посмотреть по адресу:
- Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)


#### Автор: [Горин Евгений](https://github.com/Excellent-84)