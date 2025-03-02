from repositories.ChoiceRepository import ChoiceRepository
from repositories.QuestionRepository import QuestionRepository
from fastapi import Depends, HTTPException, status
from models.QuizModel import ChoiceCreate, ChoiceResponse, ChoiceUpdate
from typing import List


class ChoiceService:
    question_repository: QuestionRepository
    choice_repository: ChoiceRepository

    def __init__(
        self,
        question_repository: QuestionRepository = Depends(),
        choice_repository: ChoiceRepository = Depends(),
    ):
        self.question_repository = question_repository
        self.choice_repository = choice_repository

    def create_choice(self, question_id: str, choice: ChoiceCreate) -> ChoiceResponse:
        question = self.question_repository.find_by_id(question_id)
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        return self.choice_repository.create(question_id, choice)

    def get_choice(self, choice_id) -> ChoiceResponse:
        choice = self.choice_repository.find_by_id(choice_id)
        if not choice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Choice not found"
            )

        return choice

    def list_choices(self, limit: int, start: int) -> List[ChoiceResponse]:
        return self.choice_repository.list(limit, start)

    def update_choice(
        self, choice_id: str, choice_update: ChoiceUpdate
    ) -> ChoiceResponse:
        choice = self.choice_repository.find_by_id(choice_id)
        if not choice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Choice not found"
            )

        return self.choice_repository.update(choice, choice_update)

    def delete_choice(self, choice_id):
        choice = self.choice_repository.find_by_id(choice_id)
        if not choice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Choice not found"
            )

        return self.choice_repository.delete(choice_id, choice)
