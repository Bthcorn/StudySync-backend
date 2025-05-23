from sqlmodel import Session, create_engine, select
from collections.abc import Generator

from config.config import settings
from config.security import get_password_hash
from models.Models import *
from models.UserModel import User, UserCreate

# add more models here

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:

    user = session.exec(
        select(User).where(User.username == settings.FIRST_SUPERUSER)
    ).first()
    if not user or user is None:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        user_obj = User.model_validate(
            user_in,
            update={
                "hashed_password": get_password_hash(user_in.password),
            },
        )
        session.add(user_obj)
        session.commit()
        session.refresh(user_obj)


def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
