from fastapi import APIRouter, Depends, HTTPException
from services.UserService import UserService
from models.UserModel import User, UserCreate, UserResponse, UserUpdateMe, UserLogin
import uuid

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, user_service: UserService = Depends()):
    try:
        return user_service.create_user(user)
    except HTTPException as e:
        raise e


@router.post("/login", response_model=UserResponse)
def login_user(user: UserLogin, user_service: UserService = Depends()):
    try:
        return user_service.authenticate(user.username, user.password)
    except HTTPException as e:
        raise e


@router.patch("/update/{id}", response_model=UserResponse)
def update_user(
    user_id: uuid.UUID, user: UserUpdateMe, user_service: UserService = Depends()
):
    try:
        return user_service.update_user(user_id, user)
    except HTTPException as e:
        raise e


@router.delete("/delete/{id}")
def delete_user(user_id: uuid.UUID, user_service: UserService = Depends()):
    try:
        return user_service.delete_user(user_id)
    except HTTPException as e:
        raise e
