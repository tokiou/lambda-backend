from models.users_models import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.future import select
from logs.handle_logger import logger
import bcrypt
# flake8: noqa


async def save_entity(db, entity) -> None:
    try:
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
    except SQLAlchemyError as sqlex:
        raise sqlex
    except Exception as ex:
        raise ex


async def user_registration(
        db,
        username: str,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str) -> None:

    try:
        role = "user"
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role
        )

        await save_entity(db, user)
        logger.info(f'{email} Registered.')
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail="User already exists")
    except Exception as ex:
        raise HTTPException(status_code=400, detail="User already exists")


async def check_user_exists(db, email: str, username: str) -> bool:
    query = select(User).where((User.username == username) | (User.email == email))
    result = await db.execute(query)
    user = result.scalars().first()
    return user is not None


async def verify_user_password(db, email: str, password: str) -> bool:
    # Get user
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()

    if user is None:
        # User not exists
        return False

    return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))