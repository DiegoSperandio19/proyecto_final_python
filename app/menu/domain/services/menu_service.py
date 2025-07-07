from fastapi import HTTPException, status
from pydantic import EmailStr
from app.menu.domain.entities.dish_entity import Dish
from app.menu.domain.repositories.dish_repository import DishRepository
from app.menu.domain.value_object.dish_dto import DishCreate
from app.shared.exceptions import InvalidName

class MenuService:
    def __init__(self, dish_repo: DishRepository):
        self.dish_repo = dish_repo

    async def create_dish(self, dish_data: DishCreate) -> Dish:
        valid_name = await self.dish_repo.validate_dish_name(dish_name=dish_data.name, restaurant_id=dish_data.restaurant_id)
        if valid_name == False:
            raise InvalidName(dish_data.name, dish_data.restaurant_id)
        
        dish_entity = Dish(
            name=dish_data.name,
            description=dish_data.description,
            category=dish_data.category,
            restaurant_id=dish_data.restaurant_id
        )

        return await self.dish_repo.add_dish(dish_entity)