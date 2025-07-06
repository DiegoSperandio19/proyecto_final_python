from fastapi import APIRouter, Depends, HTTPException
from app.restaurants.domain.services.restaurant_service import RestaurantService
from app.restaurants.domain.value_objects.created_restaurant import RestaurantCreate
from app.restaurants.domain.entities.restaurant_entity import Restaurant
from app.restaurants.infrastructure.repositories.orm_restaurant_repository import SQLAlchemyRestaurantRepository
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
restaurant_router = APIRouter()

async def get_restaurant_service(session: AsyncSession = Depends(get_session)):
    repository: SQLAlchemyRestaurantRepository = SQLAlchemyRestaurantRepository(session)
    return RestaurantService(repository)

@restaurant_router.get("/restaurants/", response_model=list[Restaurant])
async def get_restaurants(restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    restaurants= await restaurant_service.get_all_restaurants()
    return restaurants

@restaurant_router.post("/restaurants/", response_model=Restaurant)
async def add_restaurant(restaurant: RestaurantCreate, restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    return restaurant_service.add_restaurant(restaurant)