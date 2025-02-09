import uuid

from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, func
import sqlalchemy as sa
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime

if TYPE_CHECKING:
    from .FolderModel import Folder
    from .CollaborationModel import Collaboration


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
    created_at: datetime | None = Field(
        default=datetime.now(),
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
    )

    folders: List["Folder"] = Relationship(back_populates="user")
    collaborations: List["Collaboration"] = Relationship(back_populates="user")


# Properties to return via API, id is always required
class UserResponse(UserBase):
    id: uuid.UUID
