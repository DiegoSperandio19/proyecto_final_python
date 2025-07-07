#from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from app.restaurants.domain.entities.table_entity import Table
from app.restaurants.domain.repositories.table_repository import TableRepository
from app.restaurants.infrastructure.orm_entities.table_model import TableModel
from uuid import UUID



class SQLAlchemyTableRepository(TableRepository):

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_tables_by_restaurant(self,id_restaurant: UUID) -> None | Table:
        statement = select(TableModel).where(TableModel.id_restaurant == id_restaurant)
        result= await self.db.exec(statement)
        models = result.all()
        return models

    async def get_tables_by_capacity(self,capacity: int) -> None | Table:
        statement = select(TableModel).where(TableModel.capacity == capacity)
        result= await self.db.exec(statement)
        models = result.all()
        return models

    async def get_tables_by_location(self,location: str) -> None | Table:
        statement = select(TableModel).where(TableModel.location == location)
        result= await self.db.exec(statement)
        models = result.all()
        return models

    async def add_table(self, table: Table) -> Table:
        db_table = TableModel(capacity=table.capacity, location=table.location, id_restaurant=table.id_restaurant,is_eliminated=False)
        self.db.add(db_table)
        await self.db.commit()
        await self.db.refresh(db_table)
        return Table.model_validate(db_table)
        