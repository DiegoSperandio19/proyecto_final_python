from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.menu.domain.entities.preorder_entity import Preorder

class PreorderRepository(ABC):
    @abstractmethod
    async def create_preorder(self, preorder_data: Preorder) -> Preorder:
        pass