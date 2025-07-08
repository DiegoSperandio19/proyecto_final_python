from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.menu.domain.entities.preorder_entity import Preorder
from app.menu.domain.value_object.preorder_dto import PreorderOut

class PreorderRepository(ABC):
    @abstractmethod
    async def create_preorder(self, preorder_data: Preorder) -> Preorder:
        pass

    @abstractmethod
    async def get_preorders(self, reservation_id:UUID) -> List[PreorderOut]:
        pass