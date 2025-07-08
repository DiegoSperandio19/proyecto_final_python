from typing import Optional
from datetime import time
from pydantic import BaseModel, model_validator

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

    @model_validator(mode='after')
    def validate_times(self) -> 'RestaurantUpdate':
        if (self.opening_time is not None and
            self.closing_time is not None and
            self.opening_time >= self.closing_time):
            raise ValueError('Closing time must be after opening time')
        return self