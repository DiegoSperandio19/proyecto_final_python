from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.auth.domain.entities.user_entity import User
from app.auth.domain.value_objects.user_dto import UserUpdate

class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> None | User:
        pass

    @abstractmethod
    async def get_user_by_email(self, user_email: str) -> None | User:
        pass

    @abstractmethod
    async def add_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def update_user(self, user: UserUpdate) -> User:
        pass