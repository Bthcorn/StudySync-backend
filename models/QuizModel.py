from sqlmodel import Field, Relationship, SQLModel, Enum, Column, func
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid
import sqlalchemy as sa
import enum

if TYPE_CHECKING:
    from .UserModel import User
    from .FolderModel import Folder


class QuizType(str, enum.Enum):
    multiple = "multiple"
    single = "single"


class QuizMode(str, enum.Enum):
    normal = "normal"
    contest = "contest"


class QuizBase(SQLModel):
    title: str
    quiz_type: QuizType = Field(
        sa_column=Column(Enum(QuizType), default=QuizType.multiple)
    )
    mode: QuizMode = Field(sa_column=Column(Enum(QuizMode), default=QuizMode.normal))
    total_questions: int = Field(default=0)
    total_likes: int = Field(default=0)
    total_points: int = Field(default=0)
    points_to_pass: int = Field(default=0)
    time_limit: int = Field(default=0)


class Quiz(SQLModel, table=True):
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
    folder_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="folder.id", ondelete="CASCADE"
    )
    folder: Optional["Folder"] = Relationship(back_populates="quizzes")
    questions: List["Question"] = Relationship(
        back_populates="quiz", cascade_delete=True
    )
    attempts: List["UserAttempt"] = Relationship(back_populates="quiz")


class QuestionBase(SQLModel):
    question: str


class Question(QuestionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default=datetime.now(),
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
    )
    quiz_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="quiz.id", ondelete="CASCADE"
    )
    quiz: Optional[Quiz] = Relationship(back_populates="questions")
    choices: List["Choice"] = Relationship(
        back_populates="question", cascade_delete=True
    )


class ChoiceBase(SQLModel):
    choice: str
    is_answer: bool = False


class Choice(ChoiceBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=sa.DateTime(timezone=True),
    )
    question_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="question.id", ondelete="CASCADE"
    )
    question: Optional[Question] = Relationship(back_populates="choices")


class UserAttemptBase(SQLModel):
    username: str
    score: int = 0
    total_points: int = 0
    time_taken: int = 0
    passed: bool = False


class UserAttempt(UserAttemptBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    started_at: datetime = Field(
        default_factory=datetime.now,
        sa_type=sa.DateTime(timezone=True),
    )
    completed_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            sa.DateTime(timezone=True),
            onupdate=func.now(),
        ),
    )
    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.id", ondelete="CASCADE"
    )
    user: Optional["User"] = Relationship(back_populates="user_attempts")

    quiz_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="quiz.id", ondelete="SET NULL"
    )
    quiz: Optional[Quiz] = Relationship(back_populates="attempts")

    @property
    def score_percentage(self):
        return (self.score / self.total_points) * 100

    @property
    def time_taken_minutes(self):
        return self.time_taken / 60

    @property
    def time_taken_seconds(self):
        return self.time_taken % 60

    @property
    def passed_percentage(self):
        return (self.score / self.total_points) * 100 >= self.quiz.points_to_pass
