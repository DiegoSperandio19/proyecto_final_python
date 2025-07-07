from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate

class ReservationRepository(ABC):
    @abstractmethod
    async def register_reservation(self, reservation: Reservation) -> None | Reservation:
        pass
