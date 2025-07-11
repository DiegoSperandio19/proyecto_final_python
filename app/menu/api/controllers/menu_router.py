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
from app.menu.domain.entities.dish_entity import Dish
from app.menu.domain.services.menu_service import MenuService
from app.menu.domain.value_object.dish_dto import DishCreate, DishOut, DishUpdate
from app.menu.domain.value_object.preorder_dto import PreorderCreate
from app.menu.infrastructure.repositories.orm_dish_repository import SQLDishRepository
from app.menu.infrastructure.repositories.orm_preorder_repository import SQLPreorderRepository
from app.reservation.infrastructure.repositories.orm_reservation_repository import SQLReservationRepository
from app.shared.exceptions import DishNotFound, InvalidName, User

menu_router=APIRouter()

async def get_menu_service(session: AsyncSession = Depends(get_session)):
    dish_repo = SQLDishRepository(session)
    preorder_repo = SQLPreorderRepository(session)
    reservation_repo= SQLReservationRepository(session)
    return MenuService(dish_repo, preorder_repo,reservation_repo)

@menu_router.post("/dish/create", response_model=DishOut)
async def add_dish(
    dish_create: DishCreate,
    get_menu_service: Annotated[MenuService, Depends(get_menu_service)],
    get_current_user: Annotated[User, Depends(require_admin_role)]
):
    try:
        dish = await get_menu_service.create_dish(dish_create)
    except InvalidName as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    return dish

@menu_router.get("/menu/{restaurant_id}")
async def get_dish(
    restaurant_id:UUID,
    get_menu_service: Annotated[MenuService, Depends(get_menu_service)],
    get_current_user: Annotated[User, Depends(require_client_role)]

):
    dishes = await get_menu_service.get_menu_by_restaurant(restaurant_id)
    if not dishes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No dishes found for this restaurant"
        )
    return dishes

@menu_router.put("/dish/update", response_model=DishOut)
async def update_dish(
    dish_update: DishUpdate,
    get_menu_service: Annotated[MenuService, Depends(get_menu_service)],
    get_current_user: Annotated[User, Depends(require_admin_role)]
):
    try:
        dish = await get_menu_service.update_dish(dish_update)
    except DishNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except InvalidName as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    return dish

@menu_router.post("/preorder/create")
async def create_preorder(
    preorder_create: PreorderCreate,
    get_menu_service: Annotated[MenuService, Depends(get_menu_service)],
    get_current_user: Annotated[User, Depends(require_client_role)]
):
    return await get_menu_service.create_preorder(preorder_create, get_current_user)

#@menu_router.get("/dish{dish_id}")
#async def get_dish(
#    dish_id: UUID,
#    session: AsyncSession = Depends(get_session),
#):
 #   dish_repo = SQLDishRepository(session)
 #   return await dish_repo.get_dish_by_id(dish_id)


