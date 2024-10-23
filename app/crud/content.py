from models.users_models import User, UserTeamRole
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete
from fastapi import HTTPException
from typing import Optional
from uuid import UUID
from models.content_models import Idea
from models.teams_models import Team
from sqlalchemy.future import select
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


async def upload_idea(
    db,
    title: str,
    idea: str,
    team_id: UUID,
    priority: int,
    user_id: UUID,
    project_id: Optional[UUID] = None
) -> None:
        if not project_id:
             project_id = None
        try:
            idea_db = Idea(
                title=title,
                idea=idea,
                status="active",
                team_id=team_id,
                priority=priority,
                user_id=user_id,
                project_id=project_id
            )

            await save_entity(db, idea_db)
        except SQLAlchemyError as sqlex:
            raise HTTPException(status_code=400, detail=str(sqlex))
        except Exception as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        

async def get_user_teams(db, user_id: str):
    query = select(UserTeamRole).filter(UserTeamRole.user_id == user_id)
    result = await db.execute(query)
    teams = result.scalars().all()
    return teams


async def get_teams_name(db, team_ids) -> list:
    if not team_ids:
        return []


    query = select(Team).filter(Team.id == team_ids)
    result = await db.execute(query)
    
    team = result.scalars().first()
    
    return team.name


async def get_team_ideas(db, team_id: str):
    try:
        query = select(Idea).filter(Idea.team_id == team_id)
        result = await db.execute(query)
        ideas = result.scalars().all()
        return ideas
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


async def delete_team_idea(db, idea_id: str):
    query = select(Idea).where(Idea.id == idea_id)
    result = await db.execute(query)
    idea = result.scalar_one_or_none()

    if idea is None:
        raise HTTPException(status_code=404, detail="Idea not found")

    delete_query = delete(Idea).where(Idea.id == idea_id)
    await db.execute(delete_query)

    await db.commit()