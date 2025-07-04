from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.auth.domain.entities.user_entity import User

class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> None | User:
        pass

    @abstractmethod
    def get_user_by_email(self, user_email: str) -> None | User:
        pass

    @abstractmethod
    def add_user(self, user: User) -> User:
        pass