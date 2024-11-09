from pydantic import BaseModel
from typing import Optional


class Team(BaseModel):
    team_name: Optional[str] = None
    team_id: Optional[str] = None