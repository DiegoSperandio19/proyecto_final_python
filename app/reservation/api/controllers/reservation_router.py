from datetime import timedelta
from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.auth.api.dto.token_dto import Token
from app.auth.domain.entities.user_entity import User
from app.auth.infraestructure.utils.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, require_admin_role, require_client_role
from app.db import get_session
from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.services.reservation_service import ReservationService
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate
from app.reservation.infrastructure.repositories.orm_reservation_repository import SQLReservationRepository
from app.restaurants.infrastructure.repositories.orm_table_repository import SQLAlchemyTableRepository
from app.shared.exceptions import HoursReservation, TableNotFound

reservation_router=APIRouter()

async def get_reservation_service(session: AsyncSession = Depends(get_session)):
    reservation_repo =  SQLReservationRepository(session)
    table_repo = SQLAlchemyTableRepository(session)
    return ReservationService(reservation_repo, table_repo)

@reservation_router.post("/register")
async def add_dish(
    reservation: ReservationCreate,
    get_reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
    get_current_user: Annotated[User, Depends(require_client_role)]
):
    try:
        reservation = await get_reservation_service.create_reservation(reservation, user_id=get_current_user.id)
    except HoursReservation as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except TableNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return reservation

