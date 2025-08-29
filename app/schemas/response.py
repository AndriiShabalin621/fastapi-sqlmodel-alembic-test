from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

from app.models.answer import Answer


class MessageResponse(BaseModel):
    message: str


class DeleteResponse(MessageResponse):
    deleted_id: int
    timestamp: datetime


class QuestionWithAnswersResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    answers: list[Answer] = []
