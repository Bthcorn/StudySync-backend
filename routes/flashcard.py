from fastapi import APIRouter, Depends, HTTPException
import uuid
from models.FlashcardModel import FlashcardCreate, FlashcardResponse, FlashcardUpdate, TermCreate, TermResponse, TermUpdate
from services.FlashcardService import FlashcardService
from typing import List


router = APIRouter(prefix="/flashcard", tags=["flashcard"])

@router.post("/", response_model=FlashcardResponse)
def create_flashcard(folder_id: uuid.UUID, flashcard: FlashcardCreate, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.create_flashcard(folder_id, flashcard)
    except HTTPException as e:
        raise e

@router.get("/{flashcard_id}", response_model=FlashcardResponse)
def get_flashcard(flashcard_id: uuid.UUID, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.get_flashcard(flashcard_id)
    except HTTPException as e:
        raise e

@router.get("/", response_model=List[FlashcardResponse])
def get_flashcards(flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.get_flashcards()
    except HTTPException as e:
        raise e

@router.patch("/{flashcard_id}", response_model=FlashcardResponse)
def update_flashcard(flashcard_id: uuid.UUID, flashcard: FlashcardUpdate, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.update_flashcard(flashcard_id, flashcard)
    except HTTPException as e:
        raise e

@router.delete("/{flashcard_id}", response_model=FlashcardResponse)
def delete_flashcard(flashcard_id: uuid.UUID, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.delete_flashcard(flashcard_id)
    except HTTPException as e:
        raise e

@router.post("/{flashcard_id}/term", response_model=TermResponse)
def create_term(flashcard_id: uuid.UUID, term: TermCreate, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.create_term(flashcard_id, term)
    except HTTPException as e:
        raise e

@router.get("/{flashcard_id}/term", response_model=List[TermResponse])
def get_terms(flashcard_id: uuid.UUID, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.get_terms(flashcard_id)
    except HTTPException as e:
        raise e

@router.get("/term/{term_id}", response_model=TermResponse)
def get_term(term_id: uuid.UUID, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.get_term(term_id)
    except HTTPException as e:
        raise e

@router.patch("/term/{term_id}", response_model=TermResponse)
def update_term(term_id: uuid.UUID, term: TermUpdate, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.update_term(term_id, term)
    except HTTPException as e:
        raise e

@router.delete("/term/{term_id}", response_model=TermResponse)
def delete_term(term_id: uuid.UUID, flashcard_service: FlashcardService = Depends()):
    try:
        return flashcard_service.delete_term(term_id)
    except HTTPException as e:
        raise e

