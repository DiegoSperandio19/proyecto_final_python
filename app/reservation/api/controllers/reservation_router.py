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
from app.menu.infrastructure.repositories.orm_preorder_repository import SQLPreorderRepository
from app.reservation.domain.entities.reservation_entity import Reservation
from app.reservation.domain.services.reservation_service import ReservationService
from app.reservation.domain.value_objects.reservation_dto import ReservationCreate, ReservationOut
from app.reservation.infrastructure.repositories.orm_reservation_repository import SQLReservationRepository
from app.restaurants.infrastructure.repositories.orm_restaurant_repository import SQLAlchemyRestaurantRepository
from app.restaurants.infrastructure.repositories.orm_table_repository import SQLAlchemyTableRepository
from app.shared.exceptions import HourConflict, HoursReservation, ReservationNotFound, ReservationPermissionDenied, TableNotFound

reservation_router=APIRouter()

async def get_reservation_service(session: AsyncSession = Depends(get_session)):
    reservation_repo =  SQLReservationRepository(session)
    table_repo = SQLAlchemyTableRepository(session)
    restaurant_repo = SQLAlchemyRestaurantRepository(session)
    dish_repo = SQLPreorderRepository(session)
    return ReservationService(reservation_repo, table_repo, restaurant_repo, dish_repo)

@reservation_router.post("/register", response_model=ReservationOut, status_code=status.HTTP_201_CREATED)
async def create_reservation(
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
    except HourConflict as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    return reservation

@reservation_router.put("/cancel/{reservation_id}", response_model=ReservationOut, status_code=status.HTTP_200_OK)
async def cancel_reservation(
    reservation_id: UUID,
    get_reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
    get_current_user: Annotated[User, Depends(require_client_role)]
):
    try:
        reservation = await get_reservation_service.cancel_reservation(reservation_id, get_current_user)
    except ReservationNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ReservationPermissionDenied as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HourConflict as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    return reservation

@reservation_router.get("/all_reservations", status_code=status.HTTP_200_OK)
async def get_all_reservations(
    get_reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
    get_current_user: Annotated[User, Depends(require_admin_role)]
):
    return await get_reservation_service.get_all_reservations()

@reservation_router.get("/active_reservations", status_code=status.HTTP_200_OK)
async def get_active_reservations(
    get_reservation_service: Annotated[ReservationService, Depends(get_reservation_service)],
    get_current_user: Annotated[User, Depends(require_client_role)]
):
    return await get_reservation_service.get_active_reservations(get_current_user)