from fastapi import APIRouter, Depends
from typing import Dict
from crud.content import upload_idea, get_team_ideas, delete_team_idea, update_team_idea
from services.haandle_token import JWTBearer
from uuid import UUID
from schemas.content_schemas import Ideas, UpdateIdea
from sqlalchemy.ext.asyncio import AsyncSession
from crud.db import get_session
# flake8: noqa

content_router = APIRouter(prefix="/lambda")


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
async def get_ideas(team_id: str, user_id: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_session)) -> Dict:
    results = await get_team_ideas(db, team_id, user_id)
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
async def delete_idea(idea_id: str, user_id: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_session)) -> Dict:
    await delete_team_idea(db, idea_id, user_id)
    return {"message": "Idea deleted!"}


@content_router.patch("/idea/{idea_id}", dependencies=[Depends(JWTBearer)])
async def update_idea(idea_id: str, idea: UpdateIdea, user_id: str = Depends(JWTBearer()), db: AsyncSession = Depends(get_session)) -> Dict:
    await update_team_idea(db, idea_id, idea, user_id)
    return {"message": "Idea updated successfully"}



