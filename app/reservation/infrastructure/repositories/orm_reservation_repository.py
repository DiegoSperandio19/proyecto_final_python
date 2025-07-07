from typing import List
from uuid import UUID
from datetime import datetime, time, timedelta
from sqlmodel import and_, or_, select
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
    
    async def validate_table_available(self, table_id: UUID, start_time: time, end_time: time) -> bool:
        statement = select(ReservationModel).where(ReservationModel.is_eliminated==False
                    ).where(ReservationModel.status=="Pending"
                    ).where(ReservationModel.id_table==table_id
                    ).where(ReservationModel.start_time <= end_time
                    ).where(ReservationModel.end_time >= start_time)
        result = await self.db.exec(statement)
        reservation = result.first()
        if reservation:
            return False
        return True
    
    async def validate_user_available(self, user_id: UUID, start_time: time, end_time: time) -> bool:
        statement = select(ReservationModel).where(ReservationModel.is_eliminated==False
                    ).where(ReservationModel.status=="Pending"
                    ).where(ReservationModel.id_user==user_id
                    ).where(ReservationModel.start_time <= end_time
                    ).where(ReservationModel.end_time >= start_time)
        result = await self.db.exec(statement)
        reservation = result.first()
        if reservation:
            return False
        return True
    
    async def get_reservation_by_id(self, reservation_id:UUID) -> Reservation | None:
        statement = select(ReservationModel).where(ReservationModel.id==reservation_id
                        ).where(ReservationModel.is_eliminated==False).where(ReservationModel.status == "Pending")
        result = await self.db.exec(statement)
        db_reservation = result.first()
        if db_reservation is None:
            return None
        reservation= Reservation(
            id=db_reservation.id,
            id_user=db_reservation.id_user,
            id_table=db_reservation.id_table,
            start_time=db_reservation.start_time,
            end_time=db_reservation.end_time,
            status=db_reservation.status
        )
        return reservation
    
    async def change_status(self, reservation_id: UUID, status:str) -> None | Reservation:
        statement = select(ReservationModel).where(ReservationModel.id==reservation_id).where(ReservationModel.is_eliminated==False)
        result = await self.db.exec(statement)
        db_reservation = result.first()
        db_reservation.status = status
        self.db.add(db_reservation)
        await self.db.commit()
        await self.db.refresh(db_reservation)
        reservation= Reservation(
            id=db_reservation.id,
            id_user=db_reservation.id_user,
            id_table=db_reservation.id_table,
            start_time=db_reservation.start_time,
            end_time=db_reservation.end_time,
            status=db_reservation.status
        )
        return reservation