from sqlmodel import Session, select
from models.user_model import UserCreate, User, UserUpdateMe, UserResponse
from config.security import get_password_hash
from config.db import get_session
from fastapi import Depends


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user_create: UserCreate) -> UserResponse:
        db_obj = User.model_validate(
            user_create,
            update={"hashed_password": get_password_hash(user_create.password)},
        )

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj

    def find_by_username(self, username: str) -> UserResponse:
        user = self.session.exec(select(User).where(User.username == username)).first()
        return user

    def find_by_id(self, id: str) -> User:
        user = self.session.get(User, id)
        return user

    def update(self, user: User, user_update: UserUpdateMe) -> UserResponse:
        user = UserUpdateMe.model_validate(user_update)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


def get_user_repository(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)
