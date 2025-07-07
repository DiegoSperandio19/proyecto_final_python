# app/main.py
from fastapi import FastAPI, Depends
from pydantic import EmailStr
from sqlmodel import Uuid
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.api.controllers.auth_router import auth_router
from app.auth.domain.services.auth_service import AuthService
from app.auth.domain.value_objects.user_dto import UserCreate, UserOut
from app.auth.infraestructure.repositories.orm_role_repository import SQLRoleRepository
from app.auth.infraestructure.repositories.orm_user_repository import SQLUserRepository
from app.db import get_session
from fastapi.middleware.cors import CORSMiddleware

from app.restaurants.api.controllers.restaurant_router import restaurant_router
from app.restaurants.api.controllers.table_router import table_router
#from app.restaurants.domain.services.auth_service import AuthService
#from app.auth.domain.value_objects.user_dto import UserCreate, UserOut
#from app.auth.infraestructure.repositories.orm_role_repository import SQLRoleRepository






def get_app():
    app = FastAPI(
        title="API_final_proyect",
        description="final_proyect",
        version="0.1.0",
    )

    origins = ["http://localhost:4500"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(restaurant_router, prefix="/restaurants", tags=["Restaurants"])
    app.include_router(table_router, prefix="/tables", tags=["Tables"])
    return app

app = get_app()

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI!"}