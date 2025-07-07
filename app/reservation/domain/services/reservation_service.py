from datetime import datetime, time, timedelta
from uuid import UUID
from fastapi import HTTPException, status

from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.repositories.reservation_repository import ReservationRepository
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate
from app.restaurants.domain.repositories.restaurant_repository import RestaurantRepository
from app.restaurants.domain.repositories.table_repository import TableRepository
from app.shared.exceptions import HoursReservation, TableNotFound

class ReservationService:
    def __init__(self, reservation_repo: ReservationRepository, table_repo: TableRepository, restaurant_repo: RestaurantRepository):
        self.reservation_repo = reservation_repo
        self.table_repo = table_repo
        self.restaurant_repo=restaurant_repo

    async def create_reservation(self, reservation_data: ReservationCreate, user_id: UUID) -> Reservation | None:
        #validate existing table
        existing_table = await self.table_repo.get_table_by_id(reservation_data.id_table)
        if not existing_table:
            raise TableNotFound(id=reservation_data.id_table)
        
        #validate start time and end time
        date = datetime.now().date()
        start_datetime = datetime.combine(date, reservation_data.start_time)
        end_datetime = datetime.combine(date, reservation_data.end_time)
        if start_datetime >= end_datetime:
            raise HoursReservation("The start time must be before the end time")

        #validate 4 hours reservation
        time_difference: timedelta = end_datetime - start_datetime
        four_hours = timedelta(hours=4)
        if time_difference > four_hours:
            raise HoursReservation("The reservation can't exceed 4 hours")
        
        #validate start time and end time with restaurant hours
        restaurant = await self.restaurant_repo.get_restaurant_by_id(existing_table.id_restaurant)
        restaurant_opening_time = datetime.combine(date, restaurant.opening_time)
        restaurant_closing_time = datetime.combine(date, restaurant.closing_time)
        validate_start_time = start_datetime >= restaurant_opening_time and start_datetime < restaurant_closing_time
        validate_end_time = end_datetime > restaurant_opening_time and end_datetime <= restaurant_closing_time
        if not (validate_start_time and validate_end_time):
            raise HoursReservation("The reservation time must be within the restaurant's opening hours")
        
        #validate if the table is available
        if not await self.reservation_repo.validate_table_available(reservation_data.id_table, reservation_data.start_time, reservation_data.end_time):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The table is not available for the selected time"
            )

        reservation_entity = Reservation(
            id_user=user_id,
            id_table=reservation_data.id_table,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time
        )
        return await self.reservation_repo.register_reservation(reservation_entity)