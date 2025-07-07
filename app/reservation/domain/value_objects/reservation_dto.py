from datetime import time
from pydantic import BaseModel
from uuid import UUID



class ReservationCreate(BaseModel):
    id_user: UUID 
    id_table: UUID 
    start_time: time
    end_time: time