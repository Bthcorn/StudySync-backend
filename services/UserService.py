from models.UserModel import UserCreate, UserResponse, UserUpdateMe
from repositories.UserRepository import (
    UserRepository,
)
from fastapi import HTTPException, Depends, status
from config.security import verify_password
from typing import Optional, List


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()):
        self.user_repository = user_repository

    def create_user(self, user_create: UserCreate) -> UserResponse:
        user = self.user_repository.find_by_username(user_create.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        return self.user_repository.create(user_create)

    def authenticate(self, username: str, password: str) -> UserResponse:
        user = self.user_repository.find_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )

        return user

    def list_users(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 10,
        startIndex: Optional[int] = 0,
    ) -> List[UserResponse]:
        return self.user_repository.list(name, pageSize, startIndex)

    def get_user(self, id: str) -> UserResponse:
        user = self.user_repository.find_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    def update_user(self, id: str, user_update: UserUpdateMe) -> UserResponse:
        user = self.user_repository.find_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return self.user_repository.update(user, user_update)

    def delete_user(self, id: str) -> None:
        user = self.user_repository.find_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return self.user_repository.delete(id, user)
