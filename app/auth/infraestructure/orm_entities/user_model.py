from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.auth.domain.entities.user_entity import Role

class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str =Field(nullable=False, unique=True)
    hashed_password: str =Field(nullable=False)
    name: str =Field(nullable=False)
    role: str = Field(default=Role.CLIENT.value, nullable=False)