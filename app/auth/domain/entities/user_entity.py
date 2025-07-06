from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from app.auth.domain.entities.role_entity import Role

class User(BaseModel):
    id: UUID | None =None #para cuando se crea un usuario, no se tiene el id
    email: EmailStr
    hashed_password: str
    name: str 
    role: Role | None

    model_config = ConfigDict(
        from_attributes=True
    )