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