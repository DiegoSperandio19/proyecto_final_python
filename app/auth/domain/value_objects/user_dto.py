from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.auth.domain.entities.user_entity import Role

class UserCreate(BaseModel):
    email: EmailStr
    password: str    
    name: str

class UserUpdate(BaseModel):
    new_email: EmailStr | None=None
    new_password: str | None=None
    new_name: str | None=None

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    role:Role

    # Configuración de Pydantic para que funcione correctamente con objetos de ORM/Dominio
    class Config:
        # FastAPI usa esto internamente con el response_model
        from_attributes = True
