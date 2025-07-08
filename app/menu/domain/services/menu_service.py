from fastapi import HTTPException, status
from pydantic import EmailStr
from app.auth.domain.entities.user_entity import User
from app.menu.domain.entities.dish_entity import Dish
from app.menu.domain.entities.preorder_entity import Preorder
from app.menu.domain.repositories.dish_repository import DishRepository
from app.menu.domain.repositories.preorder_repository import PreorderRepository
from app.menu.domain.value_object.dish_dto import DishCreate, DishOut, DishUpdate
from app.menu.domain.value_object.preorder_dto import ListDishes, PreorderCreate, PreorderListOut, PreorderOut
from app.reservation.domain.repositories.reservation_repository import ReservationRepository
from app.shared.exceptions import DishNotFound, InvalidName, ReservationNotFound

class MenuService:
    def __init__(self, dish_repo: DishRepository, preorder_repo: PreorderRepository, reservation_repo: ReservationRepository):
        self.dish_repo = dish_repo
        self.preorder_repo= preorder_repo
        self.reservation_repo=reservation_repo

    async def create_dish(self, dish_data: DishCreate) -> Dish | None:
        valid_name = await self.dish_repo.validate_dish_name(dish_name=dish_data.name, restaurant_id=dish_data.restaurant_id)
        if valid_name == False:
            raise InvalidName(dish_data.name, dish_data.restaurant_id)
        
        dish_entity = Dish(
            name=dish_data.name,
            description=dish_data.description,
            category=dish_data.category,
            restaurant_id=dish_data.restaurant_id
        )

        return await self.dish_repo.add_dish(dish_entity)
    
    async def get_menu_by_restaurant(self, restaurant_id: str) -> list[Dish] | None:
        return await self.dish_repo.get_dishes_by_restaurant(restaurant_id)
    
    async def update_dish(self, dish_data: DishUpdate) -> Dish | None:
        existing_dish = await self.dish_repo.get_dish_by_id(dish_id=dish_data.id)
        if not existing_dish:
            raise DishNotFound(dish_data.id)
        
        if dish_data.new_name:
            if existing_dish.name != dish_data.new_name:
                valid_name = await self.dish_repo.validate_dish_name(dish_name=dish_data.new_name, restaurant_id=existing_dish.restaurant_id)
                if valid_name == False:
                    raise InvalidName(dish_data.new_name, existing_dish.restaurant_id)
                existing_dish.name=dish_data.new_name

        if dish_data.new_description:
            if existing_dish.description!=dish_data.new_description:
                existing_dish.description=dish_data.new_description

        if dish_data.new_category:
            if existing_dish.category!=dish_data.new_category:
                existing_dish.category=dish_data.new_category

        return await self.dish_repo.update_dish(existing_dish)
    
    async def create_preorder(self, preorder_data: PreorderCreate, user: User) -> None:
        existing_reservation = await self.reservation_repo.get_reservation_by_id(preorder_data.id_reservation)
        if not existing_reservation:
            raise ReservationNotFound(preorder_data.id_reservation)
        
        cant_dishes = 0
        for dish in preorder_data.dishes:
            cant_dishes += dish.n_dishes
        if cant_dishes > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You can only preorder up to 5 dishes."
            )
        list_preorders = []
        for dish in preorder_data.dishes:
            existing_dish = await self.dish_repo.get_dish_by_id(dish_id=dish.id_dish)
            if not existing_dish:
                raise DishNotFound(dish.id_dish)
            preorder=Preorder(
                id_reservation=preorder_data.id_reservation,
                id_user=user.id,
                id_table=existing_reservation.id_table,
                id_dish=dish.id_dish,
                n_dishes=dish.n_dishes
            )
            preorder_created = await self.preorder_repo.create_preorder(preorder)
            preorder_append = PreorderOut(
                id_preorder=preorder_created.id,
                id_dish=preorder_created.id_dish,
                n_dishes=preorder_created.n_dishes
            )
            list_preorders.append(preorder_append)

        dish_out = PreorderListOut(
            id_reservation=preorder_data.id_reservation,
            id_user=user.id,
            id_table=existing_reservation.id_table,
            list_preorders=list_preorders
        )
        
        return dish_out