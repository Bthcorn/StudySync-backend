from sqlmodel import Field, Relationship, SQLModel, Enum, Column, func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid
import sqlalchemy as sa
import enum
from .QuizModel import Quiz
from .FlashcardModel import Flashcard
from .NoteModel import Note
from .CollaborationModel import Collaboration

if TYPE_CHECKING:
    from .UserModel import User
    from .CollaborationModel import Collaboration
    from .QuizModel import Quiz
    from .FlashcardModel import Flashcard
    from .NoteModel import Note


class FolderAccess(str, enum.Enum):
    private = "private"
    public = "public"


class FolderBase(SQLModel):
    name: str = Field(index=True, max_length=50)
    accesss: FolderAccess = Field(
        sa_column=Column(Enum(FolderAccess), default=FolderAccess.private)
    )
    total_items: int = Field(default=0)
    total_likes: int = Field(default=0)
    img_url: Optional[str] = None


class FolderCreate(FolderBase):
    pass


# Database model
class Folder(FolderBase, table=True):
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
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    user: Optional["User"] = Relationship(back_populates="folders")
    collaborations: List["Collaboration"] = Relationship(
        back_populates="folder", cascade_delete=True
    )
    quizzes: List["Quiz"] = Relationship(back_populates="folder", cascade_delete=True)
    flashcards: List["Flashcard"] = Relationship(
        back_populates="folder", cascade_delete=True
    )
    notes: List["Note"] = Relationship(back_populates="folder", cascade_delete=True)


class FolderResponse(FolderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: Optional[uuid.UUID]
    collaborations: List["Collaboration"]
    quizzes: List["Quiz"]
    flashcards: List["Flashcard"]
    notes: List["Note"]

    class Config:
        from_attributes = True
