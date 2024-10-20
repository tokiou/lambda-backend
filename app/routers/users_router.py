from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Annotated
from crud.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from crud.users import user_registration, check_user_exists, get_user_by_username
from utils.register_utils import hash_password, verify_password
from pydantic import BaseModel, EmailStr
from logs.handle_logger import logger
from services.haandle_token import JWTBearer
from services.haandle_token import create_access_token
# flake8: noqa

user_router = APIRouter(prefix="/lambda")


class AsdModel(BaseModel):
    asd: str


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class Token(BaseModel):
    access_token: str
    token_type: str


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user-login")


@user_router.post("/user-register")
async def register_users(user: UserCreate,
                         db: AsyncSession = Depends(get_session)
                         ) -> Dict[str, str]:

    if await check_user_exists(db, user.username, user.email):
        logger.error(f'Username {user.username} or user email {user.email} already exists')
        raise HTTPException(status_code=400, detail="User already exists")


    # Hash password
    password_hash = await hash_password(user.password)

    # Register user
    await user_registration(db, user.username, user.email, password_hash,
                            user.first_name, user.last_name)

    return {"message": "created"}


@user_router.post("/user-login")
async def login_for_acesss_token(
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: AsyncSession = Depends(get_session)) -> Token:
    user = await get_user_by_username(db, form_data.username)
    if not user or not await verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = await create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return Token(access_token=access_token, token_type="bearer")



@user_router.post("/protected", dependencies=[Depends(JWTBearer())])
async def read_protected(item: AsdModel) -> Dict[str, str]:
    return {"message": item.asd}