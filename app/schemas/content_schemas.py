from typing import Optional
from pydantic import BaseModel


class Ideas(BaseModel):
    idea: str
    title: str
    project_id: Optional[str] = None
    priority: int
    team_id: str


class UpdateIdea(BaseModel):
    idea: str
    title: Optional[str] = None
    priority: Optional[int] = None
    team_id: Optional[str] = None
    status: Optional[str] = None


class Projects(BaseModel):
    name: str
    description: Optional[str] = None
    team_id: str


class ProjectOptional(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    team_id: Optional[str] = None