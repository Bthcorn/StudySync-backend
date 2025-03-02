from sqlmodel import Session, select
from fastapi import Depends
from config.db import get_db_session
from models.QuizModel import QuizCreate, Quiz, QuizUpdate
from typing import List


class QuizRepository:
    session: Session

    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def create(self, folder_id: str, quiz: QuizCreate) -> Quiz:
        db_obj = Quiz.model_validate(
            quiz,
            update={"folder_id": folder_id},
        )

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def find_by_id(self, id: str) -> Quiz:
        quiz = self.session.get(Quiz, id)
        return quiz

    def find_by_folder_id(self, folder_id: str) -> List[Quiz]:
        quizzes = self.session.exec(
            select(Quiz).where(Quiz.folder_id == folder_id)
        ).all()
        return quizzes

    def list(self, limit: int, start: int) -> Quiz:
        quizzes = self.session.exec(select(Quiz).offset(start).limit(limit)).all()
        return quizzes

    def update(self, quiz: Quiz, quiz_update: QuizUpdate) -> Quiz:
        quiz_data = quiz_update.model_dump(exclude_unset=True)
        quiz = Quiz.sqlmodel_update(quiz, obj=quiz_data)
        self.session.add(quiz)
        self.session.commit()
        self.session.refresh(quiz)
        return quiz

    def delete(self, id: str, quiz: Quiz) -> None:
        quiz = self.session.get(Quiz, id)
        self.session.delete(quiz)
        self.session.commit()
        self.session.flush()
        return None
