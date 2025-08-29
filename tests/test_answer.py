from uuid import UUID
import pytest
from httpx import AsyncClient
from app.models import Question
from app.models import Answer


class TestAnswerAPI:
    """Тесты для Answer API"""

    @pytest.mark.asyncio
    async def test_create_answer(
        self, async_client: AsyncClient, test_question_with_answers: Question
    ):
        """Создание ответа"""
        data = {
            "text": "To leave the world more interesting than we found it",
            "user_id": "f56be3a6-26d1-4f2f-a97d-55f0ab4afa2e",
        }
        response = await async_client.post(
            f"/questions/{test_question_with_answers.id}/answers", json=data
        )
        json = response.json()
        assert response.status_code == 200
        assert json["text"] == data["text"]
        assert json["user_id"] == data["user_id"]
        assert json["question_id"] == test_question_with_answers.id

    @pytest.mark.asyncio
    async def test_get_answer(
        self, async_client: AsyncClient, test_question_with_answers: Question
    ):
        """Получение ответа"""
        answer = test_question_with_answers.answers[0]
        response = await async_client.get(f"/answers/{answer.id}")
        json_data = response.json()
        assert response.status_code == 200
        assert json_data["id"] == answer.id
        assert json_data["text"] == answer.text
        assert json_data["question_id"] == answer.question_id
        assert UUID(json_data["user_id"]) == answer.user_id

    @pytest.mark.asyncio
    async def test_delete_answer(
        self,
        async_client: AsyncClient,
        test_question_with_answers: Question,
        test_session,
    ):
        """Удаление ответа"""
        answer_id = test_question_with_answers.answers[0].id
        response = await async_client.delete(f"/answers/{answer_id}")
        db_question = await test_session.get(Answer, answer_id)
        json_data = response.json()
        assert response.status_code == 200
        assert json_data["deleted_id"] == answer_id
        assert db_question is None
