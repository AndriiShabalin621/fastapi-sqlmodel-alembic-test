from pathlib import Path
from uuid import UUID
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
import logging
from sqlalchemy.orm import selectinload
from sqlmodel import select
from dotenv import load_dotenv
from app.main import app
from app.db import get_session
from app.models.question import Question
from app.models.answer import Answer
import os
from app.models import SQLModel


@pytest.fixture(autouse=True)
def load_dotenv_() -> None:
    load_dotenv()


@pytest.fixture(scope="session")
def test_database_url():
    """Фикстура для получения test database URL из переменных окружения"""
    host = os.getenv("DB_HOST_TEST", "localhost")
    port = os.getenv("DB_PORT_TEST", "5432")
    name = os.getenv("DB_NAME_TEST", "questions_and_answers_test")
    user = os.getenv("DB_USER_TEST", "postgres")
    password = os.getenv("DB_PASS_TEST", "postgres")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


@pytest.fixture(autouse=True)
def change_logging_level():
    logging.disable(logging.INFO)


@pytest.fixture(scope="function")
async def test_engine(test_database_url: str):
    """Создаем engine для тестовой БД и создаем таблицы"""
    engine = create_async_engine(test_database_url, echo=True, future=True)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest.fixture(scope="function")
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для тестовой сессии"""
    async with test_engine.connect() as conn:
        transaction = await conn.begin()

        AsyncTestingSessionLocal = sessionmaker(
            bind=conn, class_=AsyncSession, expire_on_commit=False, autoflush=False
        )

        async with AsyncTestingSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

        await transaction.rollback()


@pytest.fixture(scope="function")
async def override_get_session(test_session: AsyncSession):
    """Фикстура для переопределения зависимости get_session"""

    async def _override_get_session():
        yield test_session

    return _override_get_session


@pytest.fixture(scope="function")
async def async_client(override_get_session):
    """Фикстура для AsyncClient с переопределенной зависимостью"""

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test/"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_question_with_answers(test_session: AsyncSession) -> Question:
    """Создает тестовый вопрос c ответами для каждого теста"""
    user_uuid = UUID("f56be3a6-26d1-4f2f-a97d-55f0ab4afa2e")

    question = Question(text="What is the meaning of life?")
    test_session.add(question)

    answers = [
        Answer(
            text="To learn, grow, and help others", question=question, user_id=user_uuid
        ),
        Answer(text="42", question=question, user_id=user_uuid),
        Answer(
            text="To find happiness and fulfillment",
            question=question,
            user_id=user_uuid,
        ),
    ]
    test_session.add(question)
    test_session.add_all(answers)
    await test_session.commit()

    result = await test_session.execute(
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.id == question.id)
    )
    return result.scalar_one()
