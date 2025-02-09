from sqlmodel import Field, Relationship, SQLModel, Enum, Column
from typing import Optional, List, TYPE_CHECKING
from pydantic import model_validator
from datetime import datetime
import uuid
import sqlalchemy as sa
import enum

if TYPE_CHECKING:
    from .UserModel import User
    from .CollaborationModel import Collaboration


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


# Database model
class Folder(FolderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default=datetime.now(),
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
    )
    updated_at: datetime | None = Field(
        default=datetime.now(),
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": lambda: sa.func.now(),
            "server_default": sa.func.now(),
        },
    )

    user_id: Optional[uuid.UUID] = Field(
        default=None, foreign_key="user.id", ondelete="SET NULL"
    )
    user: Optional["User"] = Relationship(back_populates="folders")
    collaborations: List["Collaboration"] = Relationship(back_populates="folder")

    # @model_validator(mode="after")
    # @classmethod
    # def update_updated_at(cls, obj: "Folder") -> "Folder":
    #     obj.model_config["validate_assignment"] = False

    #     if obj.updated_at:
    #         # update updated_at field
    #         obj.updated_at = datetime.now()

    #     # enable validation again
    #     obj.model_config["validate_assignment"] = True
    #     return obj
