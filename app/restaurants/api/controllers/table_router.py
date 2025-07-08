from fastapi import APIRouter, Depends, HTTPException
from app.restaurants.domain.services.table_service import TableService
from app.restaurants.domain.value_objects.created_table import TableCreate
from app.restaurants.domain.value_objects.updated_table import TableUpdate
from app.restaurants.domain.entities.table_entity import Table
from app.restaurants.infrastructure.repositories.orm_table_repository import SQLAlchemyTableRepository
from app.db import get_session
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.infraestructure.utils.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, require_admin_role, require_client_role
from typing import Annotated
from app.shared.exceptions import DishNotFound, InvalidName, User
table_router = APIRouter()

async def get_table_service(session: AsyncSession = Depends(get_session)):
    repository: SQLAlchemyTableRepository = SQLAlchemyTableRepository(session)
    return TableService(repository)

@table_router.get("/tables/id/{id_restaurant}", response_model=list[Table])
async def get_tables_by_restaurant(id_restaurant: UUID, get_current_user: Annotated[User, Depends(require_client_role)], table_service: TableService = Depends(get_table_service)):
    tables= await table_service.get_tables_by_restaurant(id_restaurant)
    return tables

@table_router.get("/tables/capacity/{capacity}", response_model=list[Table])
async def get_tables_by_capacity(capacity: int, get_current_user: Annotated[User, Depends(require_client_role)], table_service: TableService = Depends(get_table_service)):
    tables= await table_service.get_tables_by_capacity(capacity)
    return tables

@table_router.get("/tables/location/{location}", response_model=list[Table])
async def get_tables_by_location(location: str, get_current_user: Annotated[User, Depends(require_client_role)], table_service: TableService = Depends(get_table_service)):
    tables= await table_service.get_tables_by_location(location)
    return tables

@table_router.post("/tables/", response_model=Table)
async def add_table(table: TableCreate, get_current_user: Annotated[User, Depends(require_admin_role)], table_service: TableService = Depends(get_table_service)):
    table= await table_service.add_table(table)
    return table

@table_router.put("/tables/{table_id}",response_model=Table)
async def update_table(table_id: UUID, table: TableUpdate, get_current_user: Annotated[User, Depends(require_admin_role)], table_service: TableService = Depends(get_table_service)):
    table=await table_service.update_table(table_id, table)
    return table

@table_router.delete("/tables/{table_id}",response_model=Table)
async def delete_table(table_id: UUID, get_current_user: Annotated[User, Depends(require_admin_role)], table_service: TableService = Depends(get_table_service)):
    table= await table_service.soft_delete_table(table_id)
    return table