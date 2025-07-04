from fastapi import HTTPException, status
from app.auth.api.dto.user_dto import UserCreate
from app.auth.domain.entities.user_entity import User
from app.auth.domain.repositories.user_repository import UserRepository
from app.auth.infraestructure.utils import auth_utils


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_new_user(self, user_data: UserCreate) -> User:
        existing_user = await self.user_repo.get_by_email(email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado.",
            )

        hashed_password = auth_utils.get_password_hash(user_data.password)

        user_entity = User(
            email=user_data.email,
            hashed_password=hashed_password,
            name=user_data.name
        )

        return await self.user_repo.add_user(user=user_entity)