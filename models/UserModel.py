import uuid

from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel, func
from typing import Optional
from datetime import datetime


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
    created_at: datetime = Field(default=func.now())


# Properties to return via API, id is always required
class UserResponse(UserBase):
    id: uuid.UUID
