from typing import TypeVar, Generic, Type, List, Any
from sqlmodel import Session, select
from fastapi import HTTPException, status
import uuid
from abc import ABC, abstractmethod

T = TypeVar("T")

class BaseService(ABC, Generic[T]):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get(self, id: uuid.UUID) -> T:
        """Get a single record by ID."""
        pass

    @abstractmethod
    def list(self, limit: int = 10, offset: int = 0) -> List[T]:
        """List records with pagination."""
        pass

    @abstractmethod
    def create(self, obj_in: Any) -> T:
        """Create a new record."""
        pass

    @abstractmethod
    def update(self, id: uuid.UUID, obj_in: Any) -> T:
        """Update a record."""
        pass

    @abstractmethod
    def delete(self, id: uuid.UUID) -> T:
        """Delete a record."""
        pass 