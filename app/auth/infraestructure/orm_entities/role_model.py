from typing import List
from uuid import UUID, uuid4
from sqlmodel import Column, Field, Relationship, SQLModel, String
from sqlalchemy.dialects.postgresql import ARRAY


class RoleModel(SQLModel, table=True):
    __tablename__ = "role"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str =Field(nullable=False)
    scopes: list[str] = Field(sa_column=Column(ARRAY(String), nullable=False))#Poner tipo de dato del scope como lsita de string?
    users: List["UserModel"] = Relationship(back_populates="role") # type: ignore