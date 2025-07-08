from enum import Enum
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID
from app.auth.domain.entities.role_entity import Role

class Preorder(BaseModel):
    id: UUID | None =None
    id_reservation: UUID | None = None
    id_user: UUID | None = None
    id_table: UUID | None = None
    n_dishes: int

    model_config = ConfigDict(
        from_attributes=True
    )