from fastapi import APIRouter, Depends
from services.haandle_token import JWTBearer
from crud.db import get_session
from crud.content import get_user_teams, get_teams_name
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
# flake8: noqa


team_router = APIRouter(prefix="/lambda")


@team_router.get("/team", dependencies=[Depends(JWTBearer())])
async def get_teams(
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)) -> Dict:

    user_teams = await get_user_teams(db, user_id)
    teams = []

    for team_id in user_teams:
        team_name = await get_teams_name(db, team_id)
        teams.append({
            "team_id": team_id,
            "team_name": team_name
        })

    return {"teams": teams}


@team_router.post("/team", dependencies=[Depends(JWTBearer)])
async def create_teams(
    team_name: str,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict:
    pass