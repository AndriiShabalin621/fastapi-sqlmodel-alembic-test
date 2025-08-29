from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.models import Question
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import get_session
from app.models.question import QuestionCreate
from app.models.answer import Answer, AnswerCreate
from app.schemas.response import DeleteResponse, QuestionWithAnswersResponse
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/questions")


@router.get("/", response_model=list[Question])
async def get_questions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Question))
    questions = result.scalars().all()
    return questions


@router.get("/{question_id}", response_model=QuestionWithAnswersResponse)
async def get_question_with_answers(
    question_id: int, session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Question)
        .options(selectinload(Question.answers))
        .where(Question.id == question_id)
    )

    question = result.scalars().first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question


@router.post("/")
async def add_question(
    question: QuestionCreate, session: AsyncSession = Depends(get_session)
):
    question = Question(text=question.text)
    session.add(question)
    await session.commit()
    await session.refresh(question)
    return question


@router.delete("/{id}")
async def delete_question(id: int, session: AsyncSession = Depends(get_session)):
    question = await session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    await session.delete(question)
    await session.commit()
    return DeleteResponse(
        message="Question successfully deleted", deleted_id=id, timestamp=datetime.now()
    )


@router.post("/{id}/answers")
async def add_answer(
    id: int, answer: AnswerCreate, session: AsyncSession = Depends(get_session)
):
    question = await session.get(Question, id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer = Answer(text=answer.text, question_id=id, user_id=answer.user_id)
    session.add(answer)
    await session.commit()
    await session.refresh(answer)
    return answer
