# Questions and Answers API

RESTful API для управления вопросами и ответами, построенная на FastAPI с использованием PostgreSQL и Docker.

## 🚀 Технологии

- **Python 3.11** - основной язык программирования
- **FastAPI** - веб-фреймворк для построения API
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **PostgreSQL 15** - реляционная база данных
- **Alembic** - система миграций базы данных
- **Docker & Docker Compose** - контейнеризация приложения
- **AsyncPG** - асинхронный драйвер для PostgreSQL

## 📦 Установка и запуск

### Предварительные требования

- Docker и Docker Compose установленные на системе
- Git для клонирования репозитория

### Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/AndriiShabalin621/fastapi-sqlmodel-alembic-test.git
cd fastapi-sqlmodel-alembic-test
```

2. Создайте файл .env в корне проекта (при необходимости):
```
# Docker postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=questions_and_answers
DB_USER=postgres
DB_PASS=postgres


# Postgres test
DB_HOST_TEST=db
DB_PORT_TEST=5432
DB_NAME_TEST=questions_and_answers
DB_USER_TEST=postgres
DB_PASS_TEST=postgres
```
3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up -d --build
```
4. Примените миграции 
```bash
docker-compose exec web alembic upgrade head
```
### 🌐 Доступ к API
Документация:  http://localhost:8004/docs




