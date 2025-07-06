from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class Table(BaseModel):
    id_table: UUID | None =None 
    capacity: int = Field(gt=2, lt=12)
    location: str
    id_restaurant: UUID
    model_config = ConfigDict(
        from_attributes=True
    )
