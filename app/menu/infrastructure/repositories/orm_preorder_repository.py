from app.menu.domain.entities.preorder_entity import Preorder
from app.menu.domain.repositories.preorder_repository import PreorderRepository
from sqlmodel.ext.asyncio.session import AsyncSession

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