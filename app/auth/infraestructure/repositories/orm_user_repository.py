from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import joinedload
from sqlmodel import select
from app.auth.domain.entities.role_entity import Role
from app.auth.domain.entities.user_entity import User
from app.auth.domain.repositories.user_repository import UserRepository
from app.auth.domain.value_objects.user_dto import UserUpdate
from app.auth.infraestructure.orm_entities.role_model import RoleModel
from app.auth.infraestructure.orm_entities.user_model import UserModel



class SQLUserRepository(UserRepository):

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_user_by_id(self, user_id: UUID) -> None | User:
        statement = select(UserModel, RoleModel).join(RoleModel).where(UserModel.id == user_id)
        result= await self.db.exec(statement)
        row = result.first()
        user_model = row[0] 
        role_model = row[1] 
        role = Role(
            id=role_model.id,
            name=role_model.name,
            scopes=role_model.scopes
        )
        user = User(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            name=user_model.name,
            role=role
        )
        if not user:
            return None
        return user

    async def get_user_by_email(self, user_email: str) -> None | User:
        statement = select(UserModel, RoleModel).join(RoleModel).where(UserModel.email == user_email)
        result= await self.db.exec(statement)
        row = result.first()
        if row is None:
            return None
        user_model = row[0] 
        role_model = row[1] 
        role = Role(
            id=role_model.id,
            name=role_model.name,
            scopes=role_model.scopes
        )
        user = User(
            id=user_model.id,
            email=user_model.email,
            hashed_password=user_model.hashed_password,
            name=user_model.name,
            role=role
        )
        if not user:
            return None
        return user
        

    async def add_user(self, user: User) -> User:
        db_user = UserModel(email=user.email, hashed_password=user.hashed_password, name=user.name, role_id=user.role.id)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return User.model_validate(db_user)
    
    async def update_user(self, user: User) -> User:
        db_user = await self.db.get(UserModel, user.id)

        db_user.email = user.email
        db_user.hashed_password = user.hashed_password
        db_user.name = user.name
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return await self.get_user_by_id(db_user.id)