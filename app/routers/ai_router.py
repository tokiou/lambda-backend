from fastapi import APIRouter, Form
from typing import List
from ai.ai_functions import generate_creative_projects

ai_router = APIRouter(prefix="/lambda")


@ai_router.post("/brainstorming")
async def brainstroming_projects(ideas: List[str] = Form(...)) -> str:
    creative_project = await generate_creative_projects(ideas)
    return creative_project
