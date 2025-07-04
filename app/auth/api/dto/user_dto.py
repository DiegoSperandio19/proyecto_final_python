from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    password: str    
    name: str

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    name: str

    # Configuración de Pydantic para que funcione correctamente con objetos de ORM/Dominio
    class Config:
        # FastAPI usa esto internamente con el response_model
        from_attributes = True
