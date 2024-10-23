from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Dict
from crud.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from crud.users import user_registration, check_user_exists, get_user_by_username
from utils.register_utils import hash_password, verify_password
from logs.handle_logger import logger
from services.haandle_token import create_access_token, create_refresh_token, create_new_access_token
from schemas.login_schemas import UserLogin, UserCreate, Token


user_router = APIRouter(prefix="/lambda")


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
                user: UserLogin,
                db: AsyncSession = Depends(get_session)) -> Token:

    db_user = await get_user_by_username(db, user.username)

    # Verify client password with db password
    if not db_user or not await verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = await create_access_token(data={"sub": str(db_user.id)}, expires_delta=timedelta(minutes=30))
    refresh_token = await create_refresh_token(data={"sub": str(db_user.id)})

    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")


@user_router.get("/refresh-token")
async def refresh_token(request: Request) -> Token:
    try:

        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="No refresh token found")

        new_access_token = await create_new_access_token(refresh_token)
        return Token(access_token=new_access_token, token_type="bearer")

    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))



