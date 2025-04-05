from fastapi import Depends, HTTPException
from repositories.FlashcardRepository import FlashcardRepository
from repositories.TermRepository import TermRepository
from repositories.FolderRepository import FolderRepository
from models.FlashcardModel import Flashcard, FlashcardCreate, FlashcardUpdate, Term, TermCreate, TermUpdate
from typing import List
import uuid
class FlashcardService:
    folder_repository: FolderRepository
    flashcard_repository: FlashcardRepository
    term_repository: TermRepository

    def __init__(self, flashcard_repository: FlashcardRepository = Depends(), term_repository: TermRepository = Depends(), folder_repository: FolderRepository = Depends()):
        self.flashcard_repository = flashcard_repository
        self.term_repository = term_repository
        self.folder_repository = folder_repository

    def create_flashcard(self, folder_id: uuid.UUID, flashcard: FlashcardCreate) -> Flashcard:
        folder = self.folder_repository.find_by_id(folder_id)
        if not folder:
            raise HTTPException(status_code=404, detail="Folder not found")
        
        update_folder = folder
        update_folder.total_items += 1
        self.folder_repository.update(folder, update_folder)
        
        return self.flashcard_repository.create(folder_id, flashcard)
    
    def get_flashcard(self, flashcard_id: uuid.UUID) -> Flashcard:
        flashcard = self.flashcard_repository.find_by_id(flashcard_id)
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        return flashcard
    
    def list_flashcards(self, limit: int, start: int) -> List[Flashcard]:
        return self.flashcard_repository.list(limit, start)
    
    def update_flashcard(self, flashcard_id: uuid.UUID, flashcard_update: FlashcardUpdate) -> Flashcard:
        flashcard = self.flashcard_repository.find_by_id(flashcard_id)
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        return self.flashcard_repository.update(flashcard, flashcard_update)
    
    def delete_flashcard(self, flashcard_id: uuid.UUID) -> None:
        flashcard = self.flashcard_repository.find_by_id(flashcard_id)
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        return self.flashcard_repository.delete(flashcard)
    
    def create_term(self, flashcard_id: uuid.UUID, term: TermCreate) -> Term:
        flashcard = self.flashcard_repository.find_by_id(flashcard_id)
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        return self.term_repository.create(flashcard.id, term)

    def get_terms(self, flashcard_id: uuid.UUID) -> List[Term]:
        flashcard = self.flashcard_repository.find_by_id(flashcard_id)
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        return self.term_repository.find_by_flashcard_id(flashcard.id)
    
    def get_term(self, term_id: uuid.UUID) -> Term:
        term = self.term_repository.find_by_id(term_id)
        if not term:
            raise HTTPException(status_code=404, detail="Term not found")
        
        return term
    
    def list_terms(self, limit: int, start: int) -> List[Term]:
        return self.term_repository.list(limit, start)
    
    def update_term(self, term_id: uuid.UUID, term_update: TermUpdate) -> Term:
        term = self.term_repository.find_by_id(term_id)
        if not term:
            raise HTTPException(status_code=404, detail="Term not found")
        
        return self.term_repository.update(term, term_update)
    
    def delete_term(self, term_id: uuid.UUID) -> None:
        term = self.term_repository.find_by_id(term_id)
        if not term:
            raise HTTPException(status_code=404, detail="Term not found")
        
        return self.term_repository.delete(term)
    
    
    
    