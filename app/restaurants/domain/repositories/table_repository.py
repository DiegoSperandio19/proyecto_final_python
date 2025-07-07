from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.restaurants.domain.entities.table_entity import Table

class TableRepository(ABC):
    @abstractmethod
    async def get_tables_by_restaurant(self,id_restaurant) -> None | Table:
        pass

    @abstractmethod
    async def get_tables_by_capacity(self,capacity) -> None | Table:
        pass

    @abstractmethod
    async def get_tables_by_location(self,location) -> None | Table:
        pass

    @abstractmethod
    async def add_table(self, table: Table) -> Table:
        pass

    @abstractmethod
    async def get_table_by_id(self, table_id: UUID) -> None | Table:
        pass
