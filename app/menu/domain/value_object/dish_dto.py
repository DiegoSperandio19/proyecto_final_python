from pydantic import BaseModel
from uuid import UUID

from app.menu.domain.entities.dish_entity import Category

class DishCreate(BaseModel):
    name: str
    description: str
    category: Category
    restaurant_id: UUID

class DishOut(BaseModel):
    id: UUID
    name: str
    description: str
    category: Category
    restaurant_id: UUID