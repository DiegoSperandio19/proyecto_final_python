from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends
from app.auth.api.dto.token_dto import Token
from app.auth.domain.entities.user_entity import User
from app.auth.domain.services.auth_service import AuthService
from app.auth.domain.value_objects.user_dto import UserCreate, UserOut, UserUpdate
from app.auth.infraestructure.utils.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, require_admin_role, require_client_role
from app.db import get_session
from app.auth.infraestructure.repositories.orm_role_repository import SQLRoleRepository
from app.auth.infraestructure.repositories.orm_user_repository import SQLUserRepository
from app.shared.exceptions import EmailAlreadyExistsException, UserNotFound

auth_router=APIRouter()

async def get_auth_service(session: AsyncSession = Depends(get_session)):
    user_repo: SQLUserRepository = SQLUserRepository(session)
    role_repo: SQLRoleRepository = SQLRoleRepository(session)
    return AuthService(user_repo, role_repo)

@auth_router.post("/login")
async def login_for_acces_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    email = form_data.username
    password = form_data.password
    user:User = await auth_service.authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    acces_token = create_access_token(
        data ={"sub": user.email, "scopes": user.role.scopes},
        expires_delta=access_token_expires
    )
    return Token(access_token=acces_token, token_type="bearer")

@auth_router.post("/profile/create", response_model=UserOut)
async def create_profile(
    user_create: UserCreate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    try:
        user = await auth_service.register_new_user(user_create)
    except EmailAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    return user

@auth_router.put("/profile/update")
async def update_profile(
    user_update: UserUpdate,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    get_current_user: Annotated[User, Depends(require_client_role)]
):
    try:
        user = await auth_service.update_user(user_update, get_current_user.id)
    except EmailAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except UserNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    return user
    
    