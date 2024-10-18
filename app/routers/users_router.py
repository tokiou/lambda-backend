from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict
from crud.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import user_registration, check_user_exists, verify_user_password
from utils.register_utils import hash_password
from pydantic import BaseModel, EmailStr
from logs.handle_logger import logger
# flake8: noqa

user_router = APIRouter(prefix="/lambda")


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str


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
async def login(email: str = Body(...),
                password: str = Body(...),
                db: AsyncSession = Depends(get_session)) -> Dict[str, str]:
    if not await verify_user_password(db, email, password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {"message": "Login successful"}
