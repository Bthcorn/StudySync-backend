from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

M = TypeVar("M")

K = TypeVar("K")


class IRepository(Generic[M, K]):
    @abstractmethod
    def create(self, instance: M) -> M:
        pass

    @abstractmethod
    def get(self, id: K) -> M:
        pass

    @abstractmethod
    def delete(self, id: K) -> None:
        pass

    @abstractmethod
    def list(self, limit: int, start: int) -> List[M]:
        pass

    @abstractmethod
    def update(self, id: K, instance: M) -> M:
        pass
