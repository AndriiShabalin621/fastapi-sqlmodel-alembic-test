import pytest
from httpx import AsyncClient
from app.models import Question
from app.models.answer import Answer
from sqlmodel import select


class TestQuestionAPI:
    """Тесты для Question API"""

    @pytest.mark.asyncio
    async def test_create_question(self, async_client: AsyncClient, test_session):
        """Создание вопроса"""
        data = {"text": "What is the meaning of life?"}
        response = await async_client.post("/questions/", json=data)

        assert response.status_code == 200
        created_question = response.json()

        db_question = await test_session.get(Question, created_question["id"])

        assert db_question is not None
        assert db_question.text == data["text"]
        assert db_question.id == created_question["id"]

    @pytest.mark.asyncio
    async def test_get_questions(
        self, async_client: AsyncClient, test_question_with_answers: Question
    ):
        """Тест получения вопросов"""
        response = await async_client.get(f"/questions/")
        json = response.json()
        assert response.status_code == 200
        assert test_question_with_answers.id in [q["id"] for q in json]
        assert test_question_with_answers.text in [q["text"] for q in json]

    @pytest.mark.asyncio
    async def test_get_question_with_answers_success(
        self, async_client: AsyncClient, test_question_with_answers: Question
    ):
        """Тест получения существующего вопроса c ответами"""
        response = await async_client.get(f"/questions/{test_question_with_answers.id}")
        json = response.json()
        assert response.status_code == 200
        assert json["text"] == test_question_with_answers.text
        assert json["id"] == test_question_with_answers.id
        assert [answer["text"] for answer in json["answers"]] == [
            answer.text for answer in test_question_with_answers.answers
        ]

    @pytest.mark.asyncio
    async def test_delete_question_success(
        self,
        async_client: AsyncClient,
        test_question_with_answers: Question,
        test_session,
    ):
        question_id = test_question_with_answers.id
        """Тест удаления существующего вопроса c ответами"""
        response = await async_client.delete(f"/questions/{question_id}")
        db_question = await test_session.get(Question, question_id)
        answers = await test_session.execute(
            select(Answer).where(Answer.question_id == 5)
        )
        answers = answers.all()
        assert response.status_code == 200
        assert db_question is None
        assert len(answers) == 0
