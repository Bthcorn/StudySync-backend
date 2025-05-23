from fastapi import APIRouter, Depends, HTTPException
from services.AuthService import AuthService
from models.UserModel import User, UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=UserResponse)
def login_user(user: UserLogin, auth_service: AuthService = Depends()):
    try:
        return auth_service.authenticate(user.username, user.password)
    except HTTPException as e:
        raise e


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, auth_service: AuthService = Depends()):
    try:
        return auth_service.register(user)
    except HTTPException as e:
        raise e
