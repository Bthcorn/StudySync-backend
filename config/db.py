from sqlmodel import Session, create_engine, select

from config.config import settings
from models.user_model import User, UserCreate
from services.user_service import UserService

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:

    user = session.exec(select(User.username == settings.FIRST_SUPERUSER)).first()
    if not user:
        user_in = UserCreate(
            username=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user_service = UserService(session)
        user = user_service.create_user(user_in)
