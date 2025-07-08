from pydantic import BaseModel
from uuid import UUID

class ListDishes(BaseModel):
    id_dish: UUID
    n_dishes: int

class PreorderCreate(BaseModel):
    id_reservation: UUID
    dishes: list[ListDishes]

class PreorderOut(BaseModel):
    id_preorder: UUID
    n_dishes: int

class PreorderListOut(BaseModel):
    id_reservation: UUID
    id_user: UUID
    id_table: UUID
    list_preorders: list[PreorderOut]
