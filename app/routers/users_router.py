from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Dict
from crud.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import user_registration, check_user_exists, get_user_by_email
from utils.register_utils import hash_password, verify_password
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
    user = await get_user_by_email(db, email)
    if not user or not await verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": "Login successful"}
