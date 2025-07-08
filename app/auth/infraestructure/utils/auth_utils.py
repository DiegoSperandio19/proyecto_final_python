from datetime import datetime, timedelta, timezone
from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from passlib.context import CryptContext

from app.auth.api.dto.token_dto import TokenData
from app.auth.domain.entities.user_entity import User
from app.auth.infraestructure.repositories.orm_user_repository import SQLUserRepository
from app.db import get_session 

SECRET_KEY = "62e3179ebba791f7cf6eb0ad1fb938d3c58684eff005d08ef813ef81c90bb2e8"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")#OJO pendiente de si hay que acomodar para que coincida con el endpoint

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None): #data ya tendría usuario y scopes
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        required_scopes: List[str],
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_session)
    ) -> User:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        scopes: List[str] = payload.get("scopes")
        if email is None or scopes is None:
            raise credentials_exception
        token_data = TokenData(email=email, scopes=scopes)
    except jwt.InvalidTokenError:
        raise credentials_exception
    
    user_repo = SQLUserRepository(session)
    user = await user_repo.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exception
    
    required_scopes_set = set(required_scopes)
    user_scopes_set = set(token_data.scopes)
    
    if not required_scopes_set.issubset(user_scopes_set):
        raise credentials_exception
    return user

async def require_admin_role(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session)
) -> User:
    return await get_current_user(required_scopes=["user:create", "user:read", "user:update", "restaurant:read", "restaurant:create", "restaurant:update", "restaurante:delete", "table:read", "table:create", "table:update", "table:delete", "reservation:create", "reservation:update", "reservation:delete", "reservation:read", "dish:read", "dish:create", "dish:update", "dish:delete", "preorder:create", "preorder:read", "preorder:delete"], token=token, session=session)
    #OJO esa lsita de required_scopes se va actualziando (agregando cosas) según los nuevos requisitos
    #Que vayan saliendo y que el rol pueda usar

async def require_client_role(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_session)
) -> User:
    return await get_current_user(required_scopes=["user:create", "user:read", "user:update", "restaurant:read", "table:read", "reservation:create", "reservation:update", "reservation:delete", "reservation:read", "dish:read", "preorder:create", "preorder:read", "preorder:delete"], token=token, session=session)
    #OJO esa lsita de required_scopes se va actualziando (agregando cosas) según los nuevos requisitos#


#verify token?