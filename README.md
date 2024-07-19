# EasyNotes

Веб сервис, который позволяет сохранять заметки с комментариями.

API сделано на основе библиотеки `FastAPI` и `sqlalchemy` для работы с базой данных. Для сохранения конфеденциальности пользователей используется хэширование пароля в хранилище, а также OAuth2 схема при передаче пароля и аутентификация по JWT токену. Все обращения к базе данных происходят в ассинхронных функциях. Данные валидируются при помощи аннотации и схем с ипользованием `pydantic`.

## Запуск

Требования:
- Python 3.11
- Poetry
- Docker
- Docker-compose

Перед запуском создайте файл с названием `.env`, в котором будут лежать параметры окружения.
<details>
<summary><h10><i>Пример</i></h10></summary>
  
```.env
POSTGRES_DB=database
POSTGRES_HOST=localhost
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_PORT=5432

DB_CONNECT_RETRY=20
DB_POOL_SIZE=15

APP_HOST=http://127.0.0.1
APP_PORT=8080
PATH_PREFIX=/api/v1

SECRET_KEY=secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

</details>

Создание виртуального окружения и установка зависимостей:

- `poetry install`

Активация виртуального окружения:

- `poetry shell`

Развертываение базы данных

- `make db`

Проведение миграций базы данных

- `make migrate`

Запуск сервиса

- `make run`

Далее можно отрыть сайт с докумментацией сервиса и оттуда же отправлять запросы.

Ссылка на документацию сервиса будет иметь вид `APP_HOST:APP_PORT/docs` (APP_HOST, APP_PORT будут браться из файли `.env`).

Ссылка с окружением из примера [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs).
