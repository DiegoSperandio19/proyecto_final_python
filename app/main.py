# app/main.py
from fastapi import FastAPI, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.domain.services.auth_service import AuthService
from app.auth.domain.value_objects.user_dto import UserCreate, UserOut
from app.auth.infraestructure.repositories.orm_role_repository import SQLRoleRepository
from app.auth.infraestructure.repositories.orm_user_repository import SQLUserRepository
from app.db import get_session






app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI!"}

@app.post("/")
async def add_client(user_create: UserCreate, session: AsyncSession = Depends(get_session)):
    user_repo = SQLUserRepository(session)
    role_repo = SQLRoleRepository(session)
    auth_service = AuthService(user_repo, role_repo)
    return await auth_service.register_new_user(user_create)