from sqlmodel import Session, select
from fastapi import Depends
from config.db import get_db_session
from models.FlashcardModel import Term, TermCreate, TermUpdate
from typing import List

class TermRepository:
    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def create(self, flashcard_id: str, term: TermCreate) -> Term:
        db_obj = Term.model_validate(term, update={"flashcard_id": flashcard_id})
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
    
    def find_by_id(self, id: str) -> Term:
        term = self.session.exec(select(Term).where(Term.id == id)).first()
        return term
    
    def find_by_flashcard_id(self, flashcard_id: str) -> List[Term]:
        terms = self.session.exec(select(Term).where(Term.flashcard_id == flashcard_id)).all()
        return terms
    
    def list(self, limit: int, start: int) -> List[Term]:
        terms = self.session.exec(select(Term).offset(start).limit(limit)).all()
        return terms
    
    def update(self, term: Term, term_update: TermUpdate) -> Term:
        term_data = term_update.model_dump(exclude_unset=True)
        term = Term.sqlmodel_update(term, obj=term_data)
        self.session.add(term)
        self.session.commit()
        self.session.refresh(term)
    
    def delete(self, term: Term) -> None:
        self.session.delete(term)
        self.session.commit()
        self.session.flush()
        return None