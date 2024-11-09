from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete, select, update
from fastapi import HTTPException
from uuid import UUID
from models.users_models import UserTeamRole
from models.teams_models import Team
from crud.content import get_user_teams, get_user_teams_owner
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
            return team.id
        except SQLAlchemyError as sqlex:
            raise HTTPException(status_code=401, detail=str(sqlex))
        except Exception as ex:
            raise HTTPException(status_code=401, detail=str(ex))


async def delete_team(
        db,
        team_id: str,
        user_id: str
):
    user_teams = await get_user_teams_owner(db, user_id)
    uuid_strings = [str(uuid) for uuid in user_teams]
    if team_id not in uuid_strings:
        raise HTTPException(status_code=401, detail="You don't have permission to delete this team")
    delete_query_team = delete(Team).where(Team.id == team_id)
    delete_query_teamrole = delete(UserTeamRole).where(UserTeamRole.team_id == team_id)
    await db.execute(delete_query_teamrole)
    await db.execute(delete_query_team)
    await db.commit()


async def assing_userteam_role(
          db,
          user_id: UUID,
          team_id: UUID,
          role: str,
) -> None:
    try:
        userteamrole = UserTeamRole(
            user_id=user_id,
            team_id=team_id,
            role=role,
        )

        await save_entity(db, userteamrole)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=401, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=401, detail=str(ex))


async def update_team_name(db, team_id: str, update_data: str, user_id: str):
    query = select(UserTeamRole).where(UserTeamRole.team_id == team_id)
    result = await db.execute(query)
    team = result.scalar_one_or_none()

    if team is None:
        raise HTTPException(status_code=403, detail="Team not found")
    
    user_teams = await get_user_teams(db, user_id)


    if team.team_id not in user_teams:
        raise HTTPException(status_code=401, detail="You don't have permission to update this team")


    update_query = (
        update(Team)
        .where(Team.id == team_id)
        .values(name=update_data)
    )

    await db.execute(update_query)
    await db.commit()