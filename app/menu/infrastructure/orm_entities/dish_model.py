from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.menu.domain.entities.dish_entity import Category

class DishModel(SQLModel, table=True):
    __tablename__ = "dish"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str =Field(nullable=False)
    description: str =Field(nullable=False)
    category: str = Field(nullable=False)
    isAvailable: bool = Field(default=True, nullable=False)
    restaurant_id: UUID = Field(nullable=False, foreign_key="restaurant.id_restaurant")