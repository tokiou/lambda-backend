from typing import Optional
from pydantic import BaseModel


class Ideas(BaseModel):
    idea: str
    title: str
    project_id: Optional[str] = None
    priority: int
    team_id: str


class UpdateIdea(BaseModel):
    idea: Optional[str] = None
    title: Optional[str] = None
    priority: Optional[int] = None
    team_id: Optional[str] = None
    status: Optional[str] = None