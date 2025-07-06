from sqlalchemy.orm import Session
from app.restaurants.domain.value_objects.created_restaurant import RestaurantCreate
from app.restaurants.domain.entities.restaurant_entity import Restaurant
from app.restaurants.domain.repositories.restaurant_repository import RestaurantRepository
from app.restaurants.infrastructure.orm_entities.restaurant_model import RestaurantModel, SessionLocal

class SQLAlchemyRestaurantRepository(RestaurantRepository):
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_all_restaurants(self) -> list[Restaurant]:
        restaurants = self.db.query(RestaurantModel).all()
        return [Restaurant.from_orm(restaurant) for restaurant in restaurants]

    def add_restaurant(self, restaurant: RestaurantCreate) -> Restaurant:
        db_restaurant = RestaurantModel(name=restaurant.name, location=restaurant.location, opening_time=restaurant.opening_time, closing_time=restaurant.closing_time)
        self.db.add(db_restaurant)
        self.db.commit()
        self.db.refresh(db_restaurant)
        return Restaurant.from_orm(db_restaurant)