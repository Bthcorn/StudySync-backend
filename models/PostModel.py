from sqlmodel import Field, Relationship, SQLModel, Column, func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid
import sqlalchemy as sa

if TYPE_CHECKING:
    from .UserModel import User


class PostBase(SQLModel):
    question: str
    is_solved: bool = False


class Post(PostBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=sa.DateTime(timezone=True),
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            sa.DateTime(timezone=True),
            onupdate=func.now(),
        ),
    )

    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    user: Optional["User"] = Relationship(back_populates="posts")
    post_replies: List["PostReply"] = Relationship(
        back_populates="post", cascade_delete=True
    )


class PostReplyBase(SQLModel):
    answer: str
    is_accepted: bool = False


class PostReply(PostReplyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=sa.DateTime(timezone=True),
    )
    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            sa.DateTime(timezone=True),
            onupdate=func.now(),
        ),
    )
    post_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="post.id", ondelete="CASCADE"
    )
    post: Optional[Post] = Relationship(back_populates="post_replies")
    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    user: Optional["User"] = Relationship(back_populates="post_replies")
