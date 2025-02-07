from sqlmodel import Session, select
from models.UserModel import UserCreate, User, UserUpdateMe, UserResponse
from config.security import get_password_hash
from config.db import get_db_session
from fastapi import Depends
from typing import List, Optional


class UserRepository:
    session: Session

    def __init__(self, session: Session = Depends(get_db_session)):
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

    def find_by_id(self, id: str) -> UserResponse:
        user = self.session.get(User, id)
        return user

    def list(
        self, name: Optional[str], limit: Optional[int], start: Optional[int]
    ) -> List[UserResponse]:
        users = self.session.exec(select(User).offset(start).limit(limit)).all()
        print(users)
        return users

    def update(self, user: User, user_update: UserUpdateMe) -> UserResponse:
        user_data = user_update.model_dump(exclude_unset=True)
        user = User.sqlmodel_update(user, obj=user_data)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, id: str, user: User) -> None:
        user = self.session.get(User, id)
        self.session.delete(user)
        self.session.commit()
        self.session.flush()
        return None
