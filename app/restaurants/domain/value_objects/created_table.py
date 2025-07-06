from pydantic import BaseModel, Field, model_validator
from uuid import UUID

class TableCreate(BaseModel):
    capacity: int
    location: str
    id_restaurant: UUID