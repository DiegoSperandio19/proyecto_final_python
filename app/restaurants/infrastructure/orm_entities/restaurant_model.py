from typing import List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from datetime import time

class RestaurantModel(SQLModel, table=True):
    __tablename__ = "restaurant"

    id_restaurant: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str =Field(nullable=False, unique=True)
    location: str =Field(nullable=False)
    opening_time: time =Field(nullable=False)
    closing_time: time =Field(nullable=False)
    is_eliminated: bool =Field(nullable=False)
    tables: List["TableModel"] = Relationship(back_populates="restaurant")