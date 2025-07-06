from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.auth.domain.entities.role_entity import Role

class RoleRepository(ABC):
    @abstractmethod
    async def get_role_by_name(self, role_name) -> None | Role:
        pass