from sqlmodel import Session, select
from fastapi import Depends
from models.FlashcardModel import Flashcard, FlashcardCreate, FlashcardUpdate
from config.db import get_db_session
from typing import List

class FlashcardRepository:
    session: Session

    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def create(self, folder_id: str, flashcard: FlashcardCreate) -> Flashcard:
        db_obj = Flashcard.model_validate(
            flashcard,
            update={"folder_id": folder_id},
        )

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def find_by_id(self, id: str) -> Flashcard:
        flashcard = self.session.exec(select(Flashcard).where(Flashcard.id == id)).first()
        return flashcard
    
    def find_by_user_id(self, user_id: str) -> List[Flashcard]:
        flashcards = self.session.exec(select(Flashcard).where(Flashcard.user_id == user_id)).all()
        return flashcards
    
    def list(self, limit: int, start: int) -> List[Flashcard]:
        flashcards = self.session.exec(select(Flashcard).offset(start).limit(limit)).all()
        return flashcards
    
    def update(self, flashcard: Flashcard, flashcard_update: FlashcardUpdate) -> Flashcard:
        flashcard_data = flashcard_update.model_dump(exclude_unset=True)
        flashcard = Flashcard.sqlmodel_update(flashcard, obj=flashcard_data)
        self.session.add(flashcard)
        self.session.commit()
        self.session.refresh(flashcard)
        return flashcard
    
    def delete(self, flashcard: Flashcard) -> None:
        self.session.delete(flashcard)
        self.session.commit()
        self.session.flush()
        return None