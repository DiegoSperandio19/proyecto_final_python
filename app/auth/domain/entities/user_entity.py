from pydantic import BaseModel, EmailStr, Field, ConfigDict
from uuid import UUID

class User(BaseModel):
    id: UUID | None =None #para cuando se crea un usuario, no se tiene el id
    email: EmailStr
    hashed_password: str
    name: str 

    model_config = ConfigDict(
        from_attributes=True
    )