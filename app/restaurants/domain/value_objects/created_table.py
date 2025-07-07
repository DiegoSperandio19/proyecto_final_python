from pydantic import BaseModel, Field, model_validator
from uuid import UUID

class TableCreate(BaseModel):
    capacity: int
    location: str
    id_restaurant: UUID
    @model_validator(mode='after')
    def validate_capacity(self) -> 'TableCreate':
        if self.capacity < 2 or self.capacity > 12:
            raise ValueError('Capacity must be between 2 and 12')
        return self