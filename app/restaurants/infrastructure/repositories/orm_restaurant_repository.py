#from uuid import UUID
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from app.restaurants.domain.entities.restaurant_entity import Restaurant
from app.restaurants.domain.repositories.restaurant_repository import RestaurantRepository
from app.restaurants.infrastructure.orm_entities.restaurant_model import RestaurantModel
from fastapi import HTTPException



class SQLAlchemyRestaurantRepository(RestaurantRepository):

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_all_restaurants(self) -> None | Restaurant:
        statement = select(RestaurantModel)
        result= await self.db.exec(statement)
        models = result.all()
        return models

    async def add_restaurant(self, restaurant: Restaurant) -> Restaurant:
        db_restaurant = RestaurantModel(name=restaurant.name, location=restaurant.location, opening_time=restaurant.opening_time, closing_time=restaurant.closing_time, is_eliminated=False)
        self.db.add(db_restaurant)
        await self.db.commit()
        await self.db.refresh(db_restaurant)
        return Restaurant.model_validate(db_restaurant)
    
    async def get_restaurant_by_id(self, restaurant_id: UUID) -> None | Restaurant:
        restaurant_db = await self.db.get(RestaurantModel, restaurant_id)
        if not restaurant_db:
            return None
        restaurant = Restaurant(
            id_restaurant=restaurant_db.id_restaurant,
            name=restaurant_db.name,
            location=restaurant_db.location,
            opening_time= restaurant_db.opening_time,
            closing_time= restaurant_db.closing_time,
            is_eliminated= restaurant_db.is_eliminated
        )
        return restaurant

    async def update_restaurant(self,restaurant_id: UUID, restaurant: Restaurant) -> Restaurant:
        db_restaurant = await self.db.get(RestaurantModel, restaurant_id)
        if not db_restaurant:
            raise HTTPException(status_code=404, detail='Restaurant not found')
        update_data=restaurant.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(db_restaurant, field, value)
        self.db.add(db_restaurant)
        await self.db.commit()
        await self.db.refresh(db_restaurant)
        return Restaurant.model_validate(db_restaurant)

    async def soft_delete_restaurant(self, restaurant_id: UUID) -> Restaurant:
        db_rest = await self.db.get(RestaurantModel, restaurant_id)
        if not db_rest:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        if db_rest.is_eliminated:
            raise HTTPException(status_code=400, detail="Restaurant already deleted")
        db_rest.is_eliminated = True
        self.db.add(db_rest)
        await self.db.commit()
        await self.db.refresh(db_rest)
        return Restaurant.model_validate(db_rest)