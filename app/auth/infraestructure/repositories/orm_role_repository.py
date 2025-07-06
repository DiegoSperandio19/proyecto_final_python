from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.auth.domain.entities.role_entity import Role
from app.auth.domain.entities.user_entity import User
from app.auth.domain.repositories.role_repository import RoleRepository
from app.auth.infraestructure.orm_entities.role_model import RoleModel

class SQLRoleRepository(RoleRepository):

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_role_by_name(self, role_name: str) -> None | Role:
        statement = select(RoleModel).where(RoleModel.name == role_name)
        result = await self.db.exec(statement)
        role = result.first()
        if not role:
            return None
        return role