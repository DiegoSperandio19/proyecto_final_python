from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID

class Table(BaseModel):
    id_table: UUID | None =None 
    capacity: int = Field()
    location: str
    id_restaurant: UUID
    is_eliminated: bool
    model_config = ConfigDict(
        from_attributes=True
    )
