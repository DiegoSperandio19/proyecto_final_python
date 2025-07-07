from time import time
from uuid import UUID, uuid4
from sqlmodel import Field, Relationship, SQLModel

from app.menu.domain.entities.dish_entity import Category

class ReservationModel(SQLModel, table=True):
    __tablename__ = "reservation"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    id_user: UUID = Field(nullable=False, foreign_key="user.id")
    id_table: UUID = Field(nullable=False, foreign_key="tables.id_table")
    start_time: time = Field(nullable=False)
    end_time: time = Field(nullable=False)
    status: str = Field(default="Pending", nullable=False)
    is_eliminated: bool = Field(default=False, nullable=False)
    