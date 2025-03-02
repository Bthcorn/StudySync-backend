from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List
from models.QuizModel import QuizCreate, QuizResponse, QuizUpdate
from services.QuizService import QuizService

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/", response_model=List[QuizResponse])
def index(
    limit: int = 10,
    start: int = 0,
    quiz_service: QuizService = Depends(),
) -> List[QuizResponse]:
    try:
        return quiz_service.list_quizzes(limit, start)
    except HTTPException as e:
        raise e


@router.post("/")
def create_quiz(
    folder_id: uuid.UUID,
    quiz: QuizCreate,
    quiz_service: QuizService = Depends(),
):
    try:
        return quiz_service.create_quiz(folder_id, quiz)
    except HTTPException as e:
        raise e


@router.get("/{quiz_id}", response_model=QuizResponse)
def get_quiz(
    quiz_id: uuid.UUID,
    quiz_service: QuizService = Depends(),
):
    try:
        return quiz_service.get_quiz(quiz_id)
    except HTTPException as e:
        raise e


@router.patch("/{quiz_id}", response_model=QuizResponse)
def update_quiz(
    quiz_id: uuid.UUID,
    quiz: QuizUpdate,
    quiz_service: QuizService = Depends(),
):
    try:
        return quiz_service.update_quiz(quiz_id, quiz)
    except HTTPException as e:
        raise e


@router.delete("/{quiz_id}")
def delete_quiz(
    quiz_id: uuid.UUID,
    quiz_service: QuizService = Depends(),
):
    try:
        return quiz_service.delete_quiz(quiz_id)
    except HTTPException as e:
        raise e
