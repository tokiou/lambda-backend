from fastapi import APIRouter
from typing import List, Dict
from ai.ai_functions import generate_creative_projects

ai_router = APIRouter(prefix="/lambda")


@ai_router.post("/brainstorming")
async def brainstroming_projects(ideas: List[str]) -> Dict[str, str]:
    creative_project = await generate_creative_projects(ideas)
    return {"possible_project": creative_project}
