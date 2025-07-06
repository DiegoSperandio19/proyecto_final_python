from fastapi import APIRouter, Depends, HTTPException
from app.restaurants.domain.services.restaurant_service import RestaurantService
from app.restaurants.domain.value_objects.created_restaurant import RestaurantCreate
from app.restaurants.domain.entities.restaurant_entity import Restaurant
from app.restaurants.infrastructure.repositories.orm_restaurant_repository import SQLAlchemyRestaurantsRepository


router = APIRouter()

async def get_restaurants_service():
    repository = SQLAlchemyRestaurantsRepository()
    return RestaurantService(repository)

@router.get("/restaurants/", response_model=list[Restaurant])
async def get_restaurants(restaurant_service: RestaurantsService = Depends(get_restaurant_service)):
    return restaurant_service.get_all_restaurants()

@router.post("/restaurants/", response_model=Restaurant)
async def add_restaurant(restaurant: RestaurantCreate, restaurant_service: RestaurantService = Depends(get_restaurant_service)):
    return restaurant_service.add_restaurant(restaurant)