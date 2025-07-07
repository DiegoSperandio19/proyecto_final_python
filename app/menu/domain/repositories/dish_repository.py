from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from app.menu.domain.entities.dish_entity import Dish

class DishRepository(ABC):
    @abstractmethod
    async def get_dish_by_id(self, dish_id: UUID) -> None | Dish:
        pass

    @abstractmethod
    async def add_dish(self, dish: Dish) -> Dish:
        pass

    @abstractmethod
    async def validate_dish_name(self, dish_name: str, restaurant_id: UUID) -> bool:
        pass

    @abstractmethod
    async def get_dishes_by_restaurant(self, restaurant_id) -> List[Dish] | None:
        pass
    #@abstractmethod
    #async def update_user(self, dish: UserUpdate) -> User:
    #    pass