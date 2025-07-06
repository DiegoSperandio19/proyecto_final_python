from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel,Relationship

from app.restaurants.domain.entities.table_entity import Table

class TableModel(SQLModel, table=True):
    __tablename__ = "tables"

    id_table: UUID = Field(default_factory=uuid4, primary_key=True)
    capacity: int =Field(nullable=False, unique=True)
    location: str =Field(nullable=False)
    id_restaurant: UUID = Field(foreign_key="restaurant.id_restaurant", nullable=False)
    restaurant: "RestaurantModel" = Relationship(back_populates="tables")
