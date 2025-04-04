import uuid

from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, func, Column
import sqlalchemy as sa
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from models.FolderModel import Folder

if TYPE_CHECKING:
    from .FolderModel import Folder
    from .CollaborationModel import Collaboration
    from .PostModel import Post, PostReply
    from .TaskModel import Task
    from .QuizModel import UserAttempt


# Shared properties
class UserBase(SQLModel):
    username: str = Field(unique=True, index=True, max_length=50)
    is_superuser: bool = False
    banner_img: Optional[str] = None
    profile_img: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)


class UserRegister(SQLModel):
    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=50)


# Properties to receive via API on update, all are optional
class UserLogin(SQLModel):
    username: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=50)


class UserUpdateMe(SQLModel):
    banner_img: Optional[str] = None
    profile_img: Optional[str] = None


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=sa.DateTime(timezone=True),
    )

    folders: List["Folder"] = Relationship(back_populates="user")
    collaborations: List["Collaboration"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)
    posts: List["Post"] = Relationship(back_populates="user")
    post_replies: List["PostReply"] = Relationship(back_populates="user")
    user_attempts: List["UserAttempt"] = Relationship(
        back_populates="user", cascade_delete=True
    )


# Properties to return via API, id is always required
class UserResponse(UserBase):
    id: uuid.UUID


class UserResponseWithFolder(UserResponse):
    folders: list[Folder] = []


class UserStatsResponse(SQLModel):
    total_folders: int
    total_flashcards: int
    total_notes: int
    total_quizzes: int
