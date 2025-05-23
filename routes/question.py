from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List
from models.QuizModel import QuestionCreate, QuestionResponse, QuestionUpdate
from services.QuestionService import QuestionService

router = APIRouter(prefix="/question", tags=["question"])


@router.post("/", response_model=QuestionResponse)
def create_question(
    quiz_id: uuid.UUID,
    question: QuestionCreate,
    question_service: QuestionService = Depends(),
):
    try:
        return question_service.create_question(quiz_id, question)
    except HTTPException as e:
        raise e


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: uuid.UUID,
    question_service: QuestionService = Depends(),
):
    try:
        return question_service.get_question(question_id)
    except HTTPException as e:
        raise e


@router.get("/", response_model=List[QuestionResponse])
def index(
    limit: int = 10,
    start: int = 0,
    question_service: QuestionService = Depends(),
) -> List[QuestionResponse]:
    try:
        return question_service.list_questions(limit, start)
    except HTTPException as e:
        raise e


@router.patch("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: uuid.UUID,
    question_update: QuestionUpdate,
    question_service: QuestionService = Depends(),
):
    try:
        return question_service.update_question(question_id, question_update)
    except HTTPException as e:
        raise e


@router.delete("/{question_id}")
def delete_question(
    question_id: uuid.UUID,
    question_service: QuestionService = Depends(),
):
    try:
        return question_service.delete_question(question_id)
    except HTTPException as e:
        raise e
