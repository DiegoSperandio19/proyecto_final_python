from pydantic import BaseModel, Field, model_validator
from datetime import time

class RestaurantCreate(BaseModel):
    name: str
    location: str
    opening_time: time
    closing_time: time
    is_eliminated: bool
    
    @model_validator(mode='after')
    def validate_times(self) -> 'RestaurantCreate':
        if self.opening_time >= self.closing_time:
            raise ValueError('Closing time must be after opening time')
        return self