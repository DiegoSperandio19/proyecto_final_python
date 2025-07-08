from fastapi import HTTPException, status
from pydantic import EmailStr

from app.auth.domain.entities.user_entity import User
from app.auth.domain.repositories.role_repository import RoleRepository
from app.auth.domain.repositories.user_repository import UserRepository
from app.auth.domain.value_objects.user_dto import UserCreate, UserUpdate
from app.auth.infraestructure.utils import auth_utils
from app.shared.exceptions import EmailAlreadyExistsException, UserNotFound


class AuthService:
    def __init__(self, user_repo: UserRepository, role_repo: RoleRepository):
        self.user_repo = user_repo
        self.role__repo = role_repo

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.user_repo.get_user_by_id(user_id)
    
    def get_user_by_email(self, user_email: str) -> User | None:
        return self.user_repo.get_user_by_email(user_email)

    async def register_new_user(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise EmailAlreadyExistsException(email=user_data.email)

        hashed_password = auth_utils.get_password_hash(user_data.password)

        role= await self.role__repo.get_role_by_name(role_name="client")

        user_entity = User(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name,
            role=role
        )

        return await self.user_repo.add_user(user=user_entity)
    
    async def update_user(self, user_data: UserUpdate, user_id) -> User:
        existing_user = await self.user_repo.get_user_by_id(user_id)
        if not existing_user:
            raise UserNotFound(user_id)
        
        if user_data.new_email:
            if existing_user.email != user_data.new_email:
                another_user = await self.user_repo.get_user_by_email(user_data.new_email)
                if another_user:
                    raise EmailAlreadyExistsException(email=user_data.new_email)
                existing_user.email = user_data.new_email

        if user_data.new_password:
            if not auth_utils.verify_password(user_data.new_password, existing_user.hashed_password):
                new_hashed_password = auth_utils.get_password_hash(user_data.new_password)
                existing_user.hashed_password = new_hashed_password

        if user_data.new_name:
            if existing_user.name != user_data.new_name:
                existing_user.name = user_data.new_name

        return await self.user_repo.update_user(existing_user)
 
    async def authenticate_user(self, email: EmailStr, password: str) -> User | None:
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            return None
        if not auth_utils.verify_password(password, user.hashed_password):
            return None
        return user