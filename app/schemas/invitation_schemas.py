from typing import Optional
from pydantic import BaseModel


class Invitation(BaseModel):
    user_invited_id: str
    team_id: str
