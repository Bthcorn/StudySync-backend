from sqlmodel import Session, select
from fastapi import Depends
from config.db import get_db_session
from models.QuizModel import ChoiceCreate, Choice, ChoiceUpdate
from typing import List


class ChoiceRepository:
    session: Session

    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def create(self, question_id: str, choice: ChoiceCreate) -> Choice:
        db_obj = Choice.model_validate(
            choice,
            update={"question_id": question_id},
        )

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def find_by_id(self, id: str) -> Choice:
        choice = self.session.get(Choice, id)
        return choice

    def find_by_question_id(self, question_id: str) -> List[Choice]:
        choices = self.session.exec(
            select(Choice).where(Choice.question_id == question_id)
        ).all()
        return choices

    def list(self, limit: int, start: int) -> Choice:
        choices = self.session.exec(select(Choice).offset(start).limit(limit)).all()
        return choices

    def update(self, choice: Choice, choice_update: ChoiceUpdate) -> Choice:
        choice_data = choice_update.model_dump(exclude_unset=True)
        choice = Choice.sqlmodel_update(choice, obj=choice_data)
        self.session.add(choice)
        self.session.commit()
        self.session.refresh(choice)
        return choice

    def delete(self, id: str, choice: Choice) -> None:
        choice = self.session.get(Choice, id)
        self.session.delete(choice)
        self.session.commit()
        self.session.flush()
        return None
