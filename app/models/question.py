from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional
from datetime import datetime


class QuestionBase(SQLModel):
    text: str = Field(min_length=10, max_length=2000)


class Question(QuestionBase, table=True):
    __tablename__ = "questions"
    id: int = Field(default=None, nullable=False, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    answers: List["Answer"] = Relationship(
        back_populates="question",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    text: str


class QuestionCreate(QuestionBase):
    pass
