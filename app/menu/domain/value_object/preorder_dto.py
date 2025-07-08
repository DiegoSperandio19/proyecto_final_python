from pydantic import BaseModel
from uuid import UUID

class PreorderCreate(BaseModel):
    id_reservation: UUID
    id_dish: UUID
    n_dishes: int

