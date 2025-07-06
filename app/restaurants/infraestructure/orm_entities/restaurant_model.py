from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel
from datetime import time

from app.auth.domain.entities.restaurant_entity import Restaurant

class RestaurantModel(SQLModel, table=True):
    __tablename__ = "restaurant"

    id_restaurant: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str =Field(nullable=False, unique=True)
    location: str =Field(nullable=False)
    opening_time: time =Field(nullable=False)
    opening_time: time =Field(nullable=False)