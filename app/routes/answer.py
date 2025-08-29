from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter
from app.models import Answer
from app.db import get_session
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.response import DeleteResponse

router = APIRouter(prefix="/answers")


@router.get("/{id}", response_model=Answer)
async def get_answer(id: int, session: AsyncSession = Depends(get_session)):
    answer = await session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    return answer


@router.delete("/{id}")
async def delete_answer(id: int, session: AsyncSession = Depends(get_session)):
    answer = await session.get(Answer, id)
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    await session.delete(answer)
    await session.commit()

    return DeleteResponse(
        message="Answer successfully deleted", deleted_id=id, timestamp=datetime.now()
    )
