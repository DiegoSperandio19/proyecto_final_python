from datetime import date, time
from typing import List
from pydantic import BaseModel
from uuid import UUID

from app.menu.domain.value_object.preorder_dto import PreorderOut
from app.reservation.domain.entities.reservation_entity import ReservationStatus



class ReservationCreate(BaseModel): 
    id_table: UUID 
    start_time: time
    end_time: time
    reservation_date: date

class ReservationOut(BaseModel): 
    id: UUID
    id_user: UUID 
    id_table: UUID 
    start_time: time
    end_time: time
    reservation_date: date
    status: ReservationStatus


class ReservationIndividualOut(BaseModel):
    reservation_id: UUID
    user_name: str
    table_id: UUID
    restaurant_name: str
    restaurant_id: UUID
    start_time: time
    end_time: time
    reservation_date: date
    status: ReservationStatus
    preorders: List[PreorderOut] = []
