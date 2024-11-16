from fastapi import APIRouter, Depends
from services.haandle_token import JWTBearer
from crud.db import get_session
from typing import Dict
from crud.content import create_project, delete_project, update_project, get_team_projects
from fastapi import HTTPException
from schemas.content_schemas import Projects, ProjectOptional
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
# flake8: noqa


project_router = APIRouter(prefix="/lambda")


@project_router.get("/project/{team_id}", dependencies=[Depends(JWTBearer())])
async def get_projects(
    team_id: str,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)) -> Dict:
    results = await get_team_projects(db, team_id, user_id)
    projects_response = [
        {
            "id": result.id,
            "name": result.name,
            "description": result.description,
            "priority": result.status
        }
        for result in results
    ]
    return {"message": projects_response}


@project_router.post("/project", dependencies=[Depends(JWTBearer)])
async def create_projects(
    project: Projects,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict:
    try:
        await create_project(db, project.name, project.description, project.team_id, user_id)
        return {"message": "Project created!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@project_router.delete("/project/{project_id}", dependencies=[Depends(JWTBearer())])
async def delete_projects(
    project_id: str,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict:
    if not project_id:
        raise HTTPException(detail='Not project_id', status_code=400)
    await delete_project(db, project_id, user_id)
    return {"message": "Project deleted"}


@project_router.patch("/project/{project_id}", dependencies=[Depends(JWTBearer)])
async def update_projects(
    project_id: str,
    project: ProjectOptional,
    user_id: str = Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session)
) -> Dict:
    await update_project(db, project_id, project, user_id)
    return {"message": "Project updated succesfully"}