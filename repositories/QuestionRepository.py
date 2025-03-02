from sqlmodel import Session, select
from fastapi import Depends
from config.db import get_db_session
from models.QuizModel import QuestionCreate, Question, QuestionUpdate
from typing import List


class QuestionRepository:
    session: Session

    def __init__(self, session: Session = Depends(get_db_session)):
        self.session = session

    def create(self, quiz_id: str, question: QuestionCreate) -> Question:
        db_obj = Question.model_validate(
            question,
            update={"quiz_id": quiz_id},
        )

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def find_by_id(self, id: str) -> Question:
        question = self.session.get(Question, id)
        return question

    def find_by_quiz_id(self, quiz_id: str) -> List[Question]:
        questions = self.session.exec(
            select(Question).where(Question.quiz_id == quiz_id)
        ).all()
        return questions

    def list(self, limit: int, start: int) -> Question:
        questions = self.session.exec(select(Question).offset(start).limit(limit)).all()
        return questions

    def update(self, question: Question, question_update: QuestionUpdate) -> Question:
        question_data = question_update.model_dump(exclude_unset=True)
        question = Question.sqlmodel_update(question, obj=question_data)
        self.session.add(question)
        self.session.commit()
        self.session.refresh(question)
        return question

    def delete(self, id: str, question: Question) -> None:
        question = self.session.get(Question, id)
        self.session.delete(question)
        self.session.commit()
        self.session.flush()
        return None
