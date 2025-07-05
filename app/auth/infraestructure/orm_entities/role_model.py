from typing import List
from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from app.auth.domain.entities.user_entity import Role
from app.auth.infraestructure.orm_entities.user_model import UserModel

class RoleModel(SQLModel, table=True):
    __tablename__ = "role"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str =Field(nullable=False)
    scopes: list[str] = Field( nullable=False)#Poner tipo de dato del scope como lsita de string?
    users: List[UserModel] = Relationship(back_populates="role")