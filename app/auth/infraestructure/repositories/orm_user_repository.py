from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.auth.domain.entities.user_entity import User
from app.auth.domain.repositories.user_repository import UserRepository
from app.auth.infraestructure.models.user_model import UserModel


class SQLUserRepository(UserRepository):

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_id(self, user_id: UUID) -> None | User:
        user= await self.db.get(UserModel, user_id)
        if not user:
            return None
        return User.model_validate(user)

    async def get_user_by_email(self, user_email: str) -> None | User:
        statement = select(UserModel).where(UserModel.email == user_email)
        result= await self.db.exec(statement)
        user=result.first()
        if not user:
            return None
        return User.model_validate(user)
        

    async def add_user(self, user: User) -> User:
        db_user = UserModel(email=user.email, hashed_password=user.hashed_password, name=user.name, role=user.role.value)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return User.model_validate(db_user)