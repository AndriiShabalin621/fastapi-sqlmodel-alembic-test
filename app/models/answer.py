from uuid import UUID
from sqlmodel import Relationship, SQLModel, Field
from typing import Optional
from datetime import datetime
from .question import Question


class AnswerBase(SQLModel):
    text: str = Field(min_length=10, max_length=2000)


class Answer(AnswerBase, table=True):
    __tablename__ = "answers"
    id: int = Field(default=None, nullable=False, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: UUID = Field(sa_column_kwargs={"index": True})
    question_id: int = Field(
        foreign_key="questions.id",
        nullable=False,
        sa_column_kwargs={"index": True},
    )

    question: Optional["Question"] = Relationship(back_populates="answers")


class AnswerCreate(AnswerBase):
    user_id: UUID
