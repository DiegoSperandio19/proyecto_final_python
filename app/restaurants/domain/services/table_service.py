from app.restaurants.domain.repositories.table_repository import TableRepository
from app.restaurants.domain.value_objects.created_table import TableCreate
from app.restaurants.domain.value_objects.updated_table import TableUpdate
from uuid import UUID
from app.restaurants.domain.entities.table_entity import Table

class TableService:
    def __init__(self, repository: TableRepository):
        self.repository = repository

    def get_tables_by_restaurant(self,id_restaurant) -> list[Table]:
        return self.repository.get_tables_by_restaurant(id_restaurant)

    def get_tables_by_capacity(self,capacity) -> list[Table]:
        return self.repository.get_tables_by_capacity(capacity)

    def get_tables_by_location(self,location) -> list[Table]:
        return self.repository.get_tables_by_location(location)

    def add_table(self, table: TableCreate) -> Table:
        return self.repository.add_table(table)

    def update_table(self, table_id: UUID, table: TableUpdate) -> Table:
        return self.repository.update_table(table_id,table)    

    def soft_delete_table(self, table_id: UUID) -> Table:
        return self.repository.soft_delete_table(table_id)  