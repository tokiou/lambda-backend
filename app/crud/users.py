from models.users_models import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.future import select
from logs.handle_logger import logger
from models.teams_models import Team
from models.users_models import UserTeamRole
# flake8: noqa


async def save_entity(db, entity) -> None:
    try:
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def user_registration(
        db,
        username: str,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str) -> str:

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
        return str(user.id)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def check_user_exists(db, email: str, username: str) -> bool:
    query = select(User).where((User.username == username) | (User.email == email))
    result = await db.execute(query)
    user = result.scalars().first()
    return user is not None


async def get_user_by_username(db, username: str):
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def create_team(
        db,
        user_id: str,
) -> str:
    try:
        team = Team(
            name="Individual_" + user_id
        )

        await save_entity(db, team)
        return team.id
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def assing_team(
        db,
        user_id: str,
        team_id: str,
) -> None:
    try:
        userteamrole = UserTeamRole(
            user_id=user_id,
            team_id=team_id,
            role="owner"
        )

        await save_entity(db, userteamrole)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))