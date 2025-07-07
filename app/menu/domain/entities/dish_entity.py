from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from app.auth.domain.entities.role_entity import Role

class Category(str, Enum):
    STARTER = "Starter"
    MAIN_COURSE = "Main"
    DESSERT = "Dessert" 
    DRINK = "Drink"

class Dish(BaseModel):
    id: UUID | None =None #para cuando se crea un usuario, no se tiene el id
    name: str
    description: str
    category: Category
    restaurant_id: UUID

    model_config = ConfigDict(
        from_attributes=True
    )