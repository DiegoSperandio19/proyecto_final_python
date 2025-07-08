from abc import ABC, abstractmethod
from typing import List
from datetime import date, datetime, time, timedelta
from uuid import UUID
from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate

class ReservationRepository(ABC):
    @abstractmethod
    async def register_reservation(self, reservation: Reservation) -> None | Reservation:
        pass

    @abstractmethod
    async def validate_table_available(self, table_id: UUID, start_time: time, end_time: time, reservation_date:date) -> bool:
        pass

    @abstractmethod
    async def validate_user_available(self, user_id: UUID, start_time: time, end_time: time, reservation_date:date) -> bool:
        pass

    @abstractmethod
    async def get_reservation_by_id(self, reservation_id:UUID) -> Reservation | None:
        pass

    @abstractmethod
    async def change_status(self, reservation_id: UUID, status:str) -> None | Reservation:
        pass

    @abstractmethod
    async def get_all_reservations(self):
        pass
