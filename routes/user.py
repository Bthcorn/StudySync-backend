from fastapi import APIRouter, Depends, HTTPException
from services.user_service import get_user_service, UserService
from models.user_model import User, UserCreate, UserResponse, UserUpdateMe

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/create", response_model=UserResponse)
def create_user(
    user: UserCreate, user_service: UserService = Depends(get_user_service)
):
    try:
        return user_service.create_user(user)
    except Exception as e:
        raise e
