from datetime import date, time
from enum import Enum
from typing import List
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID

from app.auth.domain.entities.user_entity import User
from app.menu.domain.entities.dish_entity import Dish
from app.restaurants.domain.entities.table_entity import Table

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
    reservation_date: date
    status: ReservationStatus = ReservationStatus.PENDING
    user: User | None = None
    table: Table | None = None
    #Preorder: List[Preorder] | None = None


    model_config = ConfigDict(
        from_attributes=True
    )