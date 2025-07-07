from uuid import UUID
from fastapi import HTTPException, status

from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.repositories.reservation_repository import ReservationRepository
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate

class ReservationService:
    def __init__(self, reservation_repo: ReservationRepository):
        self.reservation_repo = reservation_repo

    async def create_reservation(self, reservation_data: ReservationCreate, user_id: UUID) -> Reservation | None:
        reservation_entity = Reservation(
            id_user=user_id,
            id_table=reservation_data.id_table,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time
        )
        return await self.reservation_repo.register_reservation(reservation_entity)