from repositories.QuizRepository import QuizRepository
from repositories.FolderRepository import FolderRepository
from fastapi import Depends, HTTPException, status
from models.QuizModel import QuizCreate, QuizResponse, QuizUpdate
from typing import List


class QuizService:
    quiz_repository: QuizRepository
    folder_repository: FolderRepository

    def __init__(
        self,
        quiz_repository: QuizRepository = Depends(),
        folder_repository: FolderRepository = Depends(),
    ):
        self.quiz_repository = quiz_repository
        self.folder_repository = folder_repository

    def create_quiz(self, folder_id: str, quiz: QuizCreate) -> QuizResponse:
        folder = self.folder_repository.find_by_id(folder_id)
        if not folder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Folder not found"
            )

        return self.quiz_repository.create(folder_id, quiz)

    def get_quiz(self, quiz_id) -> QuizResponse:
        quiz = self.quiz_repository.find_by_id(quiz_id)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )

        return quiz

    def list_quizzes(self, limit: int, start: int) -> List[QuizResponse]:
        return self.quiz_repository.list(limit, start)

    def update_quiz(self, quiz_id: str, quiz_update: QuizUpdate) -> QuizResponse:
        quiz = self.quiz_repository.find_by_id(quiz_id)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )

        return self.quiz_repository.update(quiz, quiz_update)

    def delete_quiz(self, quiz_id):
        quiz = self.quiz_repository.find_by_id(quiz_id)
        if not quiz:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )

        return self.quiz_repository.delete(quiz_id, quiz)
