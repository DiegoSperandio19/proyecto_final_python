from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from app.menu.domain.entities.dish_entity import Dish
from app.menu.domain.repositories.dish_repository import DishRepository
from app.menu.infrastructure.orm_entities.dish_model import DishModel



class SQLDishRepository(DishRepository):

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_dish_by_id(self, dish_id: UUID) -> None | Dish:
        statement = select(DishModel).where(DishModel.id == dish_id).where(DishModel.isEliminated==False)
        dish_db = await self.db.get(DishModel, dish_id)
        if dish_db is None:
            return None
        dish = Dish(
            id = dish_db.id,
            name = dish_db.name,
            description= dish_db.description,
            category = dish_db.category,
            restaurant_id=dish_db.restaurant_id
        )
        return dish

    async def add_dish(self, dish: Dish) -> Dish:
        db_dish = DishModel(
            id=dish.id,
            name=dish.name,
            description=dish.description,
            category=dish.category,
            restaurant_id=dish.restaurant_id
        )
        self.db.add(db_dish)
        await self.db.commit()
        await self.db.refresh(db_dish)
        return Dish.model_validate(db_dish)
    
    async def validate_dish_name(self, dish_name: str, restaurant_id: UUID) -> bool:
        statement = select(DishModel).where(DishModel.name==dish_name).where(DishModel.restaurant_id==restaurant_id)
        result = await self.db.exec(statement)
        dish_db = result.first()
        if dish_db is None:
            return True
        return False
    
    async def get_dishes_by_restaurant(self, restaurant_id) -> List[Dish] | None:
        statement = select(DishModel).where(DishModel.restaurant_id==restaurant_id).where(DishModel.isEliminated==False)
        result = await self.db.exec(statement)
        dishes_db = result.all()
        if not dishes_db:
            return None
        list_dishes = []
        for dish_db in dishes_db:
            dish = Dish(
                id=dish_db.id,
                name=dish_db.name,
                description=dish_db.description,
                category=dish_db.category,
                restaurant_id=dish_db.restaurant_id
            )
            list_dishes.append(dish)
        return list_dishes
    
    async def update_dish(self, dish: Dish) -> Dish:
        db_dish = await self.db.get(DishModel, dish.id)
        db_dish.name= dish.name
        db_dish.description=dish.description
        db_dish.category=dish.category
        self.db.add(db_dish)
        await self.db.commit()
        await self.db.refresh(db_dish)
        dish_result = Dish(
            id=db_dish.id,
            name=db_dish.name,
            description=db_dish.description,
            category=db_dish.category,
            restaurant_id=db_dish.restaurant_id
        )
        return dish_result