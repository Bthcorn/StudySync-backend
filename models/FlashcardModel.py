from sqlmodel import Field, Relationship, SQLModel, Column, func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid
import sqlalchemy as sa

if TYPE_CHECKING:
    from .FolderModel import Folder


class FlashcardBase(SQLModel):
    name: str
    total_likes: int = Field(default=0)
    total_items: int = Field(default=0)


class Flashcard(FlashcardBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=sa.DateTime(timezone=True),
    )
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column=Column(
            sa.DateTime(timezone=True),
            onupdate=func.now(),
        ),
    )
    folder_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="folder.id", ondelete="CASCADE"
    )
    folder: Optional["Folder"] = Relationship(back_populates="flashcards")
    terms: List["Term"] = Relationship(back_populates="flashcard")


class TermBase(SQLModel):
    term: str
    definition: str


class Term(TermBase, table=True):
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
    flashcard_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="flashcard.id", ondelete="CASCADE"
    )
    flashcard: Optional["Flashcard"] = Relationship(back_populates="terms")

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(FlashcardBase):
    pass
    
class FlashcardResponse(SQLModel):
    id: uuid.UUID
    name: str
    folder_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="folder.id", ondelete="CASCADE"
    )


class TermCreate(TermBase):
    pass

class TermUpdate(TermBase):
    pass

class TermResponse(TermBase):
    id: uuid.UUID
    flashcard_id: Optional[uuid.UUID]