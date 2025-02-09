from sqlmodel import Field, Relationship, SQLModel, func, Enum, Column
from typing import Optional, List, TYPE_CHECKING
from pydantic import model_validator
from datetime import datetime
import uuid
import sqlalchemy as sa
import enum

if TYPE_CHECKING:
    from .UserModel import User
    from .FolderModel import Folder


class CollaborationRole(str, enum.Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"


class CollaborationBase(SQLModel):
    role: CollaborationRole = Field(
        sa_column=Column(Enum(CollaborationRole), default=CollaborationRole.viewer)
    )


# Database model
class Collaboration(CollaborationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    invited_at: datetime | None = Field(
        default=datetime.now(),
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
    )

    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.id", ondelete="CASCADE"
    )
    user: Optional["User"] = Relationship(back_populates="collaborations")
    folder_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="folder.id", ondelete="CASCADE"
    )
    folder: Optional["Folder"] = Relationship(back_populates="collaborations")
