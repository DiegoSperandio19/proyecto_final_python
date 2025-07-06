from app.restaurants.domain.repositories.restaurant_repository import RestaurantRepository
from app.restaurants.domain.value_objects.created_restaurant import RestaurantCreate
from app.restaurants.domain.entities.restaurant_entity import Restaurant

class RestaurantService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def get_all_restaurants(self) -> list[Restaurant]:
        return self.repository.get_all_restaurants()

    def add_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        return self.repository.add_restaurant(restaurant)