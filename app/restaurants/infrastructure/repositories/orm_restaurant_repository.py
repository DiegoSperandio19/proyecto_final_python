#from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from app.restaurants.domain.entities.restaurant_entity import Restaurant
from app.restaurants.domain.repositories.restaurant_repository import RestaurantRepository
from app.restaurants.infrastructure.orm_entities.restaurant_model import RestaurantModel



class SQLAlchemyRestaurantRepository(RestaurantRepository):

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_all_restaurants(self) -> None | Restaurant:
        statement = select(RestaurantModel)
        result= await self.db.exec(statement)
        models = result.all()
        return [
            Restaurant(
                id=m.id_restaurant,
                name=m.name,
                location=m.location,
                opening_time=m.opening_time,
                closing_time=m.closing_time,
                is_eliminated=m.is_eliminated
            )
            for m in models
        ]

    async def add_restaurant(self, restaurant: Restaurant) -> Restaurant:
        db_restaurant = RestaurantModel(name=restaurant.name, location=restaurant.location, opening_time=restaurant.opening_time, closing_time=restaurant.closing_time, is_eliminated=False)
        self.db.add(db_restaurant)
        await self.db.commit()
        await self.db.refresh(db_restaurant)
        return Restaurant.model_validate(db_restaurant)
        