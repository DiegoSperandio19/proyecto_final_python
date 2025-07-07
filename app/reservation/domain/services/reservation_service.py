from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi import HTTPException, status

from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.repositories.reservation_repository import ReservationRepository
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate
from app.restaurants.domain.repositories.table_repository import TableRepository
from app.shared.exceptions import HoursReservation, TableNotFound

class ReservationService:
    def __init__(self, reservation_repo: ReservationRepository, table_repo: TableRepository):
        self.reservation_repo = reservation_repo
        self.table_repo = table_repo

    async def create_reservation(self, reservation_data: ReservationCreate, user_id: UUID) -> Reservation | None:
        existing_table = await self.table_repo.get_table_by_id(reservation_data.id_table)
        if not existing_table:
            raise TableNotFound(id=reservation_data.id_table)
        #validate 4 hours reservation
        date = datetime.now().date()
        start_datetime = datetime.combine(date, reservation_data.start_time)
        end_datetime = datetime.combine(date, reservation_data.end_time)
        time_difference: timedelta = end_datetime - start_datetime
        four_hours = timedelta(hours=4)
        if time_difference > four_hours:
            raise HoursReservation("The reservation can't exceed 4 hours")
        
        #validate start time and end time with restaurant hours

        reservation_entity = Reservation(
            id_user=user_id,
            id_table=reservation_data.id_table,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time
        )
        return await self.reservation_repo.register_reservation(reservation_entity)