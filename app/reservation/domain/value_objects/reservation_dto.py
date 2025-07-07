from datetime import time
from pydantic import BaseModel
from uuid import UUID

from app.reservation.domain.entities.reservation_entity import ReservationStatus



class ReservationCreate(BaseModel): 
    id_table: UUID 
    start_time: time
    end_time: time

class ReservationOut(BaseModel): 
    id: UUID
    id_user: UUID 
    id_table: UUID 
    start_time: time
    end_time: time
    status: ReservationStatus