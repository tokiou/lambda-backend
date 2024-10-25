from models.users_models import User, UserTeamRole
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import delete, update
from fastapi import HTTPException
from typing import Optional
from uuid import UUID
from models.content_models import Idea
from models.teams_models import Team
from sqlalchemy.future import select
from schemas.content_schemas import UpdateIdea
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
        user_teams = await get_user_teams(db, user_id)

        print(user_teams)
        if team_id not in user_teams:
            raise HTTPException(status_code=401, detail="You don't have permission to upload this idea here")
        
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
            raise HTTPException(status_code=401, detail=str(sqlex))
        except Exception as ex:
            raise HTTPException(status_code=401, detail=str(ex))
        

async def get_user_teams(db, user_id: str):
    query = select(UserTeamRole.team_id).where(UserTeamRole.user_id == user_id)
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


async def get_team_ideas(db, team_id: str, user_id: str):
    query = select(Idea).filter(Idea.team_id == team_id, Idea.status == "active")
    result = await db.execute(query)
    ideas = result.scalars().all()
    user_teams = await get_user_teams(db, user_id)
    if team_id not in user_teams:
        raise HTTPException(status_code=401, detail="You don't have permission get this ideas.")
    return ideas


async def delete_team_idea(db, idea_id: str, user_id: str):
    query = select(Idea).where(Idea.id == idea_id)
    result = await db.execute(query)
    idea = result.scalar_one_or_none()

    if idea is None:
        raise HTTPException(status_code=404, detail="Idea not found")

    user_teams = await get_user_teams(db, user_id)


    if idea.team_id not in user_teams:
        raise HTTPException(status_code=401, detail="You don't have permission to delete this idea")

    delete_query = delete(Idea).where(Idea.id == idea_id)
    await db.execute(delete_query)

    await db.commit()


async def update_team_idea(db, idea_id: str, update_data: UpdateIdea, user_id: str):
    query = select(Idea).where(Idea.id == idea_id)
    result = await db.execute(query)
    idea = result.scalar_one_or_none()

    if idea is None:
        raise HTTPException(status_code=403, detail="Idea not found")
    
    user_teams = await get_user_teams(db, user_id)


    if idea.team_id not in user_teams:
        raise HTTPException(status_code=401, detail="You don't have permission to update this idea")

    update_data_dict = update_data.dict(exclude_unset=True)

    update_query = (
        update(Idea)
        .where(Idea.id == idea_id)
        .values(**update_data_dict)
    )

    await db.execute(update_query)
    await db.commit()

    