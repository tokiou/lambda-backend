from fastapi import APIRouter, Depends
from typing import List, Dict
from ai.ai_functions import generate_creative_projects
from services.haandle_token import JWTBearer
from pydantic import BaseModel


ai_router = APIRouter(prefix="/lambda")

class Ideas(BaseModel):
    ideas: List[str]


@ai_router.post("/brainstorming", dependencies=[Depends(JWTBearer())])
async def brainstroming_projects(ideas: Ideas, user_id: str = Depends(JWTBearer())) -> Dict[str, str]:
    print(user_id)
    creative_project = await generate_creative_projects(ideas.ideas)
    return {"possible_project": creative_project}