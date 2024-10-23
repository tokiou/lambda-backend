from fastapi import APIRouter, Depends, Request
from typing import List, Dict
from crud.content import upload_idea, get_user_teams, get_teams_name, get_team_ideas, delete_team_idea
from services.haandle_token import JWTBearer
from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Union
from models.users_models import UserTeamRole
from sqlalchemy.ext.asyncio import AsyncSession
from crud.db import get_session


content_router = APIRouter(prefix="/lambda")

class Ideas(BaseModel):
    idea: str
    title: str
    project_id: Optional[str] = None
    priority: int
    team_id: str


@content_router.post("/idea", dependencies=[Depends(JWTBearer())])
async def create_idea(
    ideas: Ideas,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict[str, str]:

    await upload_idea(
        db,
        ideas.title,
        ideas.idea,
        UUID(ideas.team_id),
        ideas.priority,
        UUID(user_id),
        ideas.project_id
        )

    return {"message": "Idea created!"}


@content_router.get("/idea", dependencies=[Depends(JWTBearer())])
async def get_ideas(team_id: str, db: AsyncSession = Depends(get_session)) -> Dict:
    results = await get_team_ideas(db, team_id)
    ideas_response = [
        {
            "id": result.id,
            "title": result.title,
            "idea": result.idea,
            "priority": result.priority
        }
        for result in results
    ]
    return {"ideas": ideas_response}


@content_router.delete("/idea/{idea_id}", dependencies=[Depends(JWTBearer)])
async def delete_idea(idea_id: str, db: AsyncSession = Depends(get_session)) -> Dict:
    await delete_team_idea(db, idea_id)
    return {"message": "Idea deleted!"}


@content_router.get("/teams", dependencies=[Depends(JWTBearer())])
async def create_idea(
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)) -> Dict:
    user_teams = await get_user_teams(db, user_id)
    teams = []
    
    for team in user_teams:
        team_id = team.team_id
        team_name = await get_teams_name(db, team_id)
        teams.append({
            "team_id": team_id,
            "team_name": team_name
        })
    
    
    return {"teams": teams}