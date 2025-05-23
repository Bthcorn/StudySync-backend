from repositories.UserRepository import UserRepository
from fastapi import HTTPException, Depends, status
from config.security import verify_password
from models.UserModel import UserCreate


class AuthService:
    userRepository = UserRepository

    def __init__(self, userRepository: UserRepository = Depends()):
        self.userRepository = userRepository

    def authenticate(self, username: str, password: str):
        user = self.userRepository.find_by_username(username)
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

    def register(self, user_create: UserCreate):
        user = self.userRepository.find_by_username(user_create.username)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
            )

        return self.userRepository.create(user_create)
