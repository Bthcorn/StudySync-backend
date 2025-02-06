from models.user_model import UserCreate, UserResponse
from repositories.user_repository import (
    UserRepository,
    get_user_repository,
)
from fastapi import HTTPException, Depends, status


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate) -> UserResponse:
        user = self.user_repository.find_by_username(user_create.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        return self.user_repository.create(user_create)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)
