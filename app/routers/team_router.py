from fastapi import APIRouter, Depends
from services.haandle_token import JWTBearer
from crud.db import get_session
from crud.content import get_user_teams, get_teams_name
from crud.team import create_team, assing_userteam_role, delete_team, update_team_name
from typing import Dict
from fastapi import HTTPException
from schemas.team_schemas import Team
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
    team: Team,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict:
    if not team.team_name:
        raise HTTPException(status_code=401, detail='Not team_id')
    team_id = await create_team(db, team.team_name)
    await assing_userteam_role(db, user_id, team_id, 'owner')
    return {"message": "Team Created"}


@team_router.delete("/team", dependencies=[Depends(JWTBearer())])
async def delete_teams(
    team: Team,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict:
    if not team.team_id:
        raise HTTPException(status_code=401, detail='Not team_id')
    await delete_team(db, team.team_id, user_id)
    return {"message": "Team deleted"}


@team_router.patch("/team/{idea_id}", dependencies=[Depends(JWTBearer)])
async def update_teams(
    team: Team,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict:
    if not team.team_id or not team.team_name:
        raise HTTPException(status_code=401, detail='Not team_id or team_name')
    await update_team_name(db, team.team_id, team.team_name, user_id)
    return {"message": "team_name updated!"}