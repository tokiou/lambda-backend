from fastapi import APIRouter, Depends
from services.haandle_token import JWTBearer
from crud.db import get_session
from typing import Dict
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import register_invitation, update_invitation_status
from schemas.invitation_schemas import Invitation
from uuid import UUID
# flake8: noqa


invitations_router = APIRouter(prefix="/lambda")


@invitations_router.post("/invitations", dependencies=[Depends(JWTBearer())])
async def send_invitation(invitation: Invitation,
                          user_id: str = Depends(JWTBearer()),
                          db: AsyncSession = Depends(get_session)) -> Dict:
    await register_invitation(db, user_id, invitation.user_invited_id, invitation.team_id)
    return {"Message": "Invitation sended!"}


@invitations_router.patch("/invitations/{invitation_id}/{status}", dependencies=[Depends(JWTBearer())])
async def accept_or_reject_invitation(
      invitation_id: str,
      status: str,
      user_id: str = Depends(JWTBearer()),
      db: AsyncSession = Depends(get_session)
) -> Dict:
     await update_invitation_status(db, user_id, invitation_id, status)
     return {"Message": f"The invitation was {status}!"}