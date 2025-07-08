from app.restaurants.domain.repositories.restaurant_repository import RestaurantRepository
from app.restaurants.domain.value_objects.created_restaurant import RestaurantCreate
from app.restaurants.domain.value_objects.updated_restaurant import RestaurantUpdate
from uuid import UUID
from app.restaurants.domain.entities.restaurant_entity import Restaurant

class RestaurantService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def get_all_restaurants(self) -> list[Restaurant]:
        return self.repository.get_all_restaurants()

    def add_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        return self.repository.add_restaurant(restaurant)

    def update_restaurant(self, restaurant_id: UUID, restaurant: RestaurantUpdate) -> Restaurant:
        return self.repository.update_restaurant(restaurant_id,restaurant)    

    def soft_delete_restaurant(self, restaurant_id: UUID) -> Restaurant:
        return self.repository.soft_delete_restaurant(restaurant_id)  