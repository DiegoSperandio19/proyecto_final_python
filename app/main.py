# app/main.py
from fastapi import FastAPI, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.api.dto.user_dto import UserCreate
from app.auth.domain.services.auth_service import AuthService
from app.auth.infraestructure.repositories.orm_user_repository import SQLUserRepository
from app.db import get_session






app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI!"}