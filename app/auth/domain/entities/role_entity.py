from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID

class RoleName(str, Enum):
    CLIENT = "client"
    ADMIN = "admin"

class Role(BaseModel):
    id: UUID | None =None #para cuando se crea un usuario, no se tiene el id
    name: RoleName 
    scopes: list[str]

    model_config = ConfigDict(
        from_attributes=True
    )