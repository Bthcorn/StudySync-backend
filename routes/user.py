from fastapi import APIRouter, Depends, HTTPException
from services.UserService import UserService
from models.UserModel import (
    User,
    UserCreate,
    UserResponse,
    UserUpdateMe,
    UserLogin,
    UserResponseWithFolder,
)
import uuid
from typing import List

router = APIRouter(prefix="/user", tags=["user"])


@router.get(
    "/",
)
def index(
    pageSize: int = 10, startIndex: int = 0, user_service: UserService = Depends()
) -> List[UserResponse]:
    try:
        return user_service.list_users(
            name=None, pageSize=pageSize, startIndex=startIndex
        )
    except HTTPException as e:
        raise e


@router.get("/{id}", response_model=UserResponse)
def get_user(id: uuid.UUID, user_service: UserService = Depends()):
    try:
        return user_service.get_user(id)
    except HTTPException as e:
        raise e

@router.get("/{id}/folders", response_model=UserResponseWithFolder)
def get_user_with_folders(id: uuid.UUID, user_service: UserService = Depends()):
    try:
        return user_service.get_user_with_folders(id)
    except HTTPException as e:
        raise e

@router.patch("/{id}", response_model=UserResponse)
def update_user(
    id: uuid.UUID, user: UserUpdateMe, user_service: UserService = Depends()
):
    try:
        return user_service.update_user(id, user)
    except HTTPException as e:
        raise e


@router.delete("/{id}")
def delete_user(id: uuid.UUID, user_service: UserService = Depends()):
    try:
        return user_service.delete_user(id)
    except HTTPException as e:
        raise e
