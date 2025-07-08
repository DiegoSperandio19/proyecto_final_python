from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel

class PreorderModel(SQLModel, table=True):
    __tablename__ = "preorder"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    id_reservation: UUID = Field(nullable=False, foreign_key="reservation.id")
    id_user: UUID = Field(nullable=False, foreign_key="user.id")
    id_table: UUID = Field(nullable=False, foreign_key="tables.id_table")
    id_dish: UUID = Field(nullable=False, foreign_key="dish.id")
    n_dishes: int = Field(nullable=False)
    is_eliminated: bool = Field(default=False, nullable=False)