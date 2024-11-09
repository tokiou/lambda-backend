from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from uuid import UUID
from models.users_models import UserTeamRole
from models.teams_models import Team
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


async def create_team(
    db,
    name: str,
) -> None:

        try:
            team = Team(
                name=name,
            )

            await save_entity(db, team)
        except SQLAlchemyError as sqlex:
            raise HTTPException(status_code=401, detail=str(sqlex))
        except Exception as ex:
            raise HTTPException(status_code=401, detail=str(ex))


async def assing_userteam(
          db,
          user_id: UUID,
          team_id: UUID,
          role: str,
) -> None:
    try:
        userteamrole = UserTeamRole(
            user_id=user_id,
            team_id=team_id,
            role=str,
        )

        await save_entity(db, userteamrole)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=401, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=401, detail=str(ex))