from sqlmodel import Session, select

from config.security import get_password_hash, verify_password
from models.user_model import User, UserCreate


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_create: UserCreate) -> User:
        db_obj = User.model_validate(
            user_create,
            update={"hashed_password": get_password_hash(user_create.password)},
        )

        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return db_obj
