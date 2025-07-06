from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.restaurants.domain.entities.restaurant_entity import Restaurant

class RestaurantRepository(ABC):
    @abstractmethod
    async def get_all_restaurants(self) -> None | Restaurant:
        pass

    @abstractmethod
    async def add_restaurant(self, user: Restaurant) -> Restaurant:
        pass

'''
    @abstractmethod
    async def update_restaurant(self, restaurant_id: UUID) -> Restaurant:
        pass
    
    @abstractmethod
    async def delete_restaurant(self, restaurant_id: UUID) -> Restaurant:
        pass

'''