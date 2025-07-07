from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.repositories.reservation_repository import ReservationRepository
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate
from app.reservation.infrastructure.orm_entities.reservation_model import ReservationModel

class SQLReservationRepository(ReservationRepository):

    def __init__(self, session: AsyncSession):
        self.db = session
    
    async def register_reservation(self, reservation: Reservation) -> None | Reservation:
        db_reservation = ReservationModel(
            id_user=reservation.id_user,
            id_table=reservation.id_table,
            start_time=reservation.start_time,
            end_time=reservation.end_time,
            status=reservation.status
        )
        self.db.add(db_reservation)
        await self.db.commit()
        await self.db.refresh(db_reservation)
        return Reservation.model_validate(db_reservation)