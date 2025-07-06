from datetime import timedelta
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.auth.api.dto.token_dto import Token
from app.auth.infraestructure.utils.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, require_admin_role, require_client_role
from app.db import get_session
from app.menu.domain.entities.dish_entity import Dish
from app.menu.domain.value_object.dish_dto import DishCreate
from app.menu.infrastructure.repositories.orm_dish_repository import SQLDishRepository

menu_router=APIRouter()



@menu_router.post("/dish")
async def add_dish(
    dish_create: DishCreate,
    session: AsyncSession = Depends(get_session)
):
    dish_repo = SQLDishRepository(session)
    dish = Dish(
        name=dish_create.name,
        description=dish_create.description,
        category=dish_create.category,
        restaurant_id=dish_create.restaurant_id
    )
    return await dish_repo.add_dish(dish)

@menu_router.get("/dish{dish_id}")
async def get_dish(
    dish_id: UUID,
    session: AsyncSession = Depends(get_session)
):
    dish_repo = SQLDishRepository(session)
    return await dish_repo.get_dish_by_id(dish_id)