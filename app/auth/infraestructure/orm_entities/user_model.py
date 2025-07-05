from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.auth.domain.entities.user_entity import Role

class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str =Field(nullable=False, unique=True)
    hashed_password: str =Field(nullable=False)
    name: str =Field(nullable=False)
    role_id: UUID = Field(default="1974ee3d-105d-4a74-9858-75d17c9822a0", nullable=False, foreign_key="role.id")
    role: Role = Relationship(back_populates="users")