from sqlmodel import Field, Relationship, SQLModel, Enum, Column, func
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid
import sqlalchemy as sa
import enum

if TYPE_CHECKING:
    from .UserModel import User


class TaskStatus(str, enum.Enum):
    todo = "todo"
    doing = "doing"
    done = "done"


class TaskBase(SQLModel):
    task: str
    status: TaskStatus = Field(
        sa_column=Column(Enum(TaskStatus), default=TaskStatus.todo)
    )


class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=sa.DateTime(timezone=True),
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            sa.DateTime(timezone=True),
            onupdate=func.now(),
        ),
    )
    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.id", ondelete="CASCADE"
    )
    user: Optional["User"] = Relationship(back_populates="tasks")
