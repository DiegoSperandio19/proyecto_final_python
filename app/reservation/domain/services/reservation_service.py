from datetime import datetime, time, timedelta
from typing import List
from uuid import UUID
from fastapi import HTTPException, status

from app.auth.domain.entities.user_entity import User
from app.menu.domain.repositories.preorder_repository import PreorderRepository
from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.repositories.reservation_repository import ReservationRepository
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate, ReservationIndividualOut
from app.restaurants.domain.repositories.restaurant_repository import RestaurantRepository
from app.restaurants.domain.repositories.table_repository import TableRepository
from app.shared.exceptions import HourConflict, HoursReservation, ReservationNotFound, ReservationPermissionDenied, TableNotFound

class ReservationService:
    def __init__(self, reservation_repo: ReservationRepository, table_repo: TableRepository, restaurant_repo: RestaurantRepository, preorder_repo = PreorderRepository):
        self.reservation_repo = reservation_repo
        self.table_repo = table_repo
        self.restaurant_repo=restaurant_repo
        self.preorder_repo= preorder_repo

    async def create_reservation(self, reservation_data: ReservationCreate, user_id: UUID) -> Reservation | None:
        #validate existing table
        existing_table = await self.table_repo.get_table_by_id(reservation_data.id_table)
        if not existing_table:
            raise TableNotFound(id=reservation_data.id_table)
        
        today = datetime.now().date()
        if reservation_data.reservation_date < today:
            raise HoursReservation("The reservation date cann't be in the past")
        
        #validate start time and end time
        start_datetime = datetime.combine(reservation_data.reservation_date, reservation_data.start_time)
        end_datetime = datetime.combine(reservation_data.reservation_date, reservation_data.end_time)

        
        now = datetime.now()
        if start_datetime < now:
            raise HoursReservation("The start time must be in the future")

        if start_datetime >= end_datetime:
            raise HoursReservation("The start time must be before the end time")

        #validate 4 hours reservation
        time_difference: timedelta = end_datetime - start_datetime
        four_hours = timedelta(hours=4)
        if time_difference > four_hours:
            raise HoursReservation("The reservation can't exceed 4 hours")
        
        #validate start time and end time with restaurant hours
        restaurant = await self.restaurant_repo.get_restaurant_by_id(existing_table.id_restaurant)
        restaurant_opening_time = datetime.combine(reservation_data.reservation_date, restaurant.opening_time)
        restaurant_closing_time = datetime.combine(reservation_data.reservation_date, restaurant.closing_time)
        validate_start_time = start_datetime >= restaurant_opening_time and start_datetime < restaurant_closing_time
        validate_end_time = end_datetime > restaurant_opening_time and end_datetime <= restaurant_closing_time
        if not (validate_start_time and validate_end_time):
            raise HoursReservation("The reservation time must be within the restaurant's opening hours")
        
        #validate if the table is available
        if not await self.reservation_repo.validate_table_available(reservation_data.id_table, reservation_data.start_time, reservation_data.end_time, reservation_data.reservation_date):
            raise HourConflict("The table is not available for the selected time")
        
        #validate if the user has an existing reservation
        if not await self.reservation_repo.validate_user_available(user_id, reservation_data.start_time, reservation_data.end_time, reservation_data.reservation_date):
            raise HourConflict("The user already has a reservation for the selected time")

        reservation_entity = Reservation(
            id_user=user_id,
            id_table=reservation_data.id_table,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time,
            reservation_date=reservation_data.reservation_date
        )
        return await self.reservation_repo.register_reservation(reservation_entity)
    
    async def cancel_reservation(self, reservation_id: UUID, user: User) -> Reservation | None:
        existing_reservation = await self.reservation_repo.get_reservation_by_id(reservation_id)
        if not existing_reservation:
            raise ReservationNotFound(reservation_id)
        if user.role.name == "client":
            if existing_reservation.id_user!= user.id:
                raise ReservationPermissionDenied("You don't have permission to cancel this reservation")
            #
            now = datetime.now()
            original_date = existing_reservation.reservation_date
            if original_date == now.date():
                start_datetime = datetime.combine(now.date(), existing_reservation.start_time)
                time_difference: timedelta = start_datetime - now
                one_hour = timedelta(hours=1)
                if time_difference < one_hour:
                    raise HourConflict("You can only cancel a reservation at least one hour before the start time")
        return await self.reservation_repo.change_status(reservation_id, "Cancelled")
        
    async def get_all_reservations(self):
        reservations: List[ReservationIndividualOut] = await self.reservation_repo.get_all_reservations()
        if not reservations:
            return []
        for reservation in reservations:
            reservation.preorders = await self.preorder_repo.get_preorders(reservation_id=reservation.reservation_id)
        return reservations