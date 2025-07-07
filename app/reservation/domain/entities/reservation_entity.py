from datetime import time
from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID

from app.menu.domain.entities.dish_entity import Dish

class ReservationStatus(str, Enum):
    PENDING  = "Pending"
    CANCELLED = "Cancelled" 
    COMPLETED = "Completed"

class Reservation(BaseModel):
    id: UUID | None =None
    id_user: UUID | None = None  
    id_table: UUID | None = None  
    start_time: time
    end_time: time
    status: ReservationStatus = ReservationStatus.PENDING
    #Preorder: List[Preorder] | None = None


    model_config = ConfigDict(
        from_attributes=True
    )