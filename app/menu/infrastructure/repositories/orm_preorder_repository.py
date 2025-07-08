from sqlmodel import select
from typing import List
from uuid import UUID
from app.menu.domain.entities.preorder_entity import Preorder
from app.menu.domain.repositories.preorder_repository import PreorderRepository
from sqlmodel.ext.asyncio.session import AsyncSession

from app.menu.domain.value_object.preorder_dto import PreorderOut, PreorderReservationOut
from app.menu.infrastructure.orm_entities.dish_model import DishModel
from app.menu.infrastructure.orm_entities.preorder_model import PreorderModel


class SQLPreorderRepository(PreorderRepository):
    def __init__(self, session: AsyncSession):
        self.db = session
    
    async def create_preorder(self, preorder_data: Preorder) -> Preorder:
        db_preorder = PreorderModel(
            id_reservation=preorder_data.id_reservation,
            id_user=preorder_data.id_user,
            id_table=preorder_data.id_table,
            id_dish=preorder_data.id_dish,
            n_dishes=preorder_data.n_dishes
        )
        self.db.add(db_preorder)
        await self.db.commit()
        await self.db.refresh(db_preorder)
        return Preorder.model_validate(db_preorder)
    
    async def get_preorders(self, reservation_id:UUID) -> List[PreorderOut]:
        statement = select(PreorderModel, DishModel).join(DishModel, PreorderModel.id_dish==DishModel.id
                ).where(PreorderModel.id_reservation==reservation_id
                ).where(PreorderModel.is_eliminated==False)
        result = await self.db.exec(statement)
        row = result.all()
        if not row:
            return []
        preorders: List[PreorderReservationOut] = []
        for preorder, dish in row:
            pre_out = PreorderReservationOut(
                id_preorder=preorder.id,
                id_dish=dish.id,
                dish_name=dish.name,
                dish_description=dish.description,
                n_dishes=preorder.n_dishes
            )
            preorders.append(pre_out)
        return preorders
            