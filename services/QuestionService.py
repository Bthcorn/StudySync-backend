from repositories.QuizRepository import QuizRepository
from repositories.QuestionRepository import QuestionRepository
from fastapi import Depends, HTTPException, status
from models.QuizModel import QuestionCreate, QuestionResponse, QuestionUpdate
from typing import List


class QuestionService:
    question_repository: QuestionRepository
    quiz_repository: QuizRepository

    def __init__(
        self,
        question_repository: QuestionRepository = Depends(),
        quiz_repository: QuizRepository = Depends(),
    ):
        self.question_repository = question_repository
        self.quiz_repository = quiz_repository

    def create_question(
        self, quiz_id: str, question: QuestionCreate
    ) -> QuestionResponse:
        quiz = self.quiz_repository.find_by_id(quiz_id)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )

        return self.question_repository.create(quiz_id, question)

    def get_question(self, question_id) -> QuestionResponse:
        question = self.question_repository.find_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        return self.question_repository.find_by_id(question_id)

    def list_questions(self, limit: int, start: int) -> List[QuestionResponse]:
        return self.question_repository.list(limit, start)

    def update_question(
        self, question_id: str, question_update: QuestionUpdate
    ) -> QuestionResponse:
        question = self.question_repository.find_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        return self.question_repository.update(question, question_update)

    def delete_question(self, question_id):
        question = self.question_repository.find_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        return self.question_repository.delete(question_id, question)
