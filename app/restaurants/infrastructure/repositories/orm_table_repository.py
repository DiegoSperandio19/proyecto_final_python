#from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from fastapi import HTTPException
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
        
    async def get_table_by_id(self, table_id: UUID) -> None | Table:
        db_table = await self.db.get(TableModel, table_id)
        if not db_table:
            return None
        table = Table(
            id_table=db_table.id_table,
            capacity=db_table.capacity,
            location=db_table.location,
            id_restaurant=db_table.id_restaurant,
            is_eliminated=db_table.is_eliminated
        )
        return table

    async def update_table(self,table_id: UUID, table: Table) -> Table:
        db_table = await self.db.get(TableModel, table_id)
        if not db_table:
            raise HTTPException(status_code=404, detail='Table not found')
        update_data=table.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(db_table, field, value)
        self.db.add(db_table)
        await self.db.commit()
        await self.db.refresh(db_table)
        return Table.model_validate(db_table)

    async def soft_delete_table(self, table_id: UUID) -> Table:
        db_table = await self.db.get(TableModel, table_id)
        if not db_table:
            raise HTTPException(status_code=404, detail="Table not found")
        if db_table.is_eliminated:
            raise HTTPException(status_code=400, detail="Table already deleted")
        db_table.is_eliminated = True
        self.db.add(db_table)
        await self.db.commit()
        await self.db.refresh(db_table)
        return Table.model_validate(db_table)
        