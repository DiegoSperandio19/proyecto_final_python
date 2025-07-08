from fastapi import APIRouter, Depends, HTTPException
from app.restaurants.domain.services.restaurant_service import RestaurantService
from app.restaurants.domain.value_objects.created_restaurant import RestaurantCreate
from app.restaurants.domain.value_objects.updated_restaurant import RestaurantUpdate
from app.restaurants.domain.entities.restaurant_entity import Restaurant
from app.restaurants.infrastructure.repositories.orm_restaurant_repository import SQLAlchemyRestaurantRepository
from uuid import UUID
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.infraestructure.utils.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, require_admin_role, require_client_role
from typing import Annotated
from app.shared.exceptions import DishNotFound, InvalidName, User
restaurant_router = APIRouter()

async def get_restaurant_service(session: AsyncSession = Depends(get_session)):
    repository: SQLAlchemyRestaurantRepository = SQLAlchemyRestaurantRepository(session)
    return RestaurantService(repository)

@restaurant_router.get("/restaurants/", response_model=list[Restaurant])
async def get_restaurants(get_current_user: Annotated[User, Depends(require_client_role)], restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    restaurants= await restaurant_service.get_all_restaurants()
    return restaurants

@restaurant_router.post("/restaurants/", response_model=Restaurant)
async def add_restaurant(get_current_user: Annotated[User, Depends(require_admin_role)], restaurant: RestaurantCreate, restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    restaurant= await restaurant_service.add_restaurant(restaurant)
    return restaurant

@restaurant_router.put("/restaurants/{restaurant_id}",response_model=Restaurant)
async def update_restaurant(get_current_user: Annotated[User, Depends(require_admin_role)],restaurant_id: UUID, restaurant: RestaurantUpdate, restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    restaurant=await restaurant_service.update_restaurant(restaurant_id, restaurant)
    return restaurant

@restaurant_router.delete("/restaurants/{restaurant_id}",response_model=Restaurant)
async def delete_restaurant(get_current_user: Annotated[User, Depends(require_admin_role)],restaurant_id: UUID,restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    restaurant= await restaurant_service.soft_delete_restaurant(restaurant_id)
    return restaurant