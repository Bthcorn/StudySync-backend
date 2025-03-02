from fastapi import APIRouter, Depends, HTTPException
import uuid
from typing import List
from models.QuizModel import ChoiceCreate, ChoiceResponse, ChoiceUpdate
from services.ChoiceService import ChoiceService

router = APIRouter(prefix="/choice", tags=["choice"])


@router.post("/", response_model=ChoiceResponse)
def create_choice(
    question_id: uuid.UUID,
    choice: ChoiceCreate,
    choice_service: ChoiceService = Depends(),
):
    try:
        return choice_service.create_choice(question_id, choice)
    except HTTPException as e:
        raise e


@router.get("/{choice_id}", response_model=ChoiceResponse)
def get_choice(
    choice_id: uuid.UUID,
    choice_service: ChoiceService = Depends(),
):
    try:
        return choice_service.get_choice(choice_id)
    except HTTPException as e:
        raise e


@router.get("/", response_model=List[ChoiceResponse])
def index(
    limit: int = 10,
    start: int = 0,
    choice_service: ChoiceService = Depends(),
) -> List[ChoiceResponse]:
    try:
        return choice_service.list_choices(limit, start)
    except HTTPException as e:
        raise e


@router.patch("/{choice_id}", response_model=ChoiceResponse)
def update_choice(
    choice_id: uuid.UUID,
    choice_update: ChoiceUpdate,
    choice_service: ChoiceService = Depends(),
):
    try:
        return choice_service.update_choice(choice_id, choice_update)
    except HTTPException as e:
        raise e


@router.delete("/{choice_id}")
def delete_choice(
    choice_id: uuid.UUID,
    choice_service: ChoiceService = Depends(),
):
    try:
        return choice_service.delete_choice(choice_id)
    except HTTPException as e:
        raise e
