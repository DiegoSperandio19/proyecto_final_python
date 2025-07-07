from datetime import timedelta
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.auth.api.dto.token_dto import Token
from app.auth.infraestructure.utils.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, require_admin_role, require_client_role
from app.db import get_session
from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate
from app.reservation.infrastructure.repositories.orm_reservation_repository import SQLReservationRepository

reservation_router=APIRouter()

@reservation_router.post("/register")
async def add_dish(
    reservation: ReservationCreate,
    session: AsyncSession = Depends(get_session)
):
    reservation_repo =  SQLReservationRepository(session)
    re = Reservation(
        id_user=reservation.id_user,
        id_table=reservation.id_table,
        start_time=reservation.start_time,
        end_time=reservation.end_time
    )
    return await reservation_repo.register_reservation(re)