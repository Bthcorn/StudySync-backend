from sqlmodel import Field, Relationship, SQLModel, Column, func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid
import sqlalchemy as sa
import enum


if TYPE_CHECKING:
    from .FolderModel import Folder


class NoteBase(SQLModel):
    name: str
    total_likes: int = Field(default=0)
    file_path: Optional[str] = None


class Note(NoteBase, table=True):
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

    folder_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="folder.id", ondelete="CASCADE"
    )
    folder: Optional["Folder"] = Relationship(back_populates="notes")
