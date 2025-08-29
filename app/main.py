from fastapi import APIRouter, Depends, FastAPI, status
from sqlmodel import select
from app.routes import question, answer
from app.middleware.logging import LoggingMiddleware


api_router = APIRouter()

api_router.include_router(question.router)
api_router.include_router(answer.router)

app = FastAPI()

app.include_router(api_router)

app.add_middleware(LoggingMiddleware)
