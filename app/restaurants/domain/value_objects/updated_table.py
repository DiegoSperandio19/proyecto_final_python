from pydantic import BaseModel, Field, model_validator
from uuid import UUID
from typing import Optional

class TableUpdate(BaseModel):
    capacity: Optional[int] = None
    location: Optional[str] = None
    id_restaurant: Optional[UUID] = None

    @model_validator(mode='after')
    def validate_capacity(self) -> 'TableUpdate':
        if self.capacity is not None and (self.capacity < 2 or self.capacity > 12):
            raise ValueError('Capacity must be between 2 and 12')
        return self
