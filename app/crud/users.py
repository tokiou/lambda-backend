from models.users_models import User
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.future import select
from logs.handle_logger import logger
from models.teams_models import Team
from models.users_models import UserTeamRole, Invitation
from crud.content import get_user_teams
from uuid import UUID
from datetime import datetime
# flake8: noqa


async def save_entity(db, entity) -> None:
    try:
        db.add(entity)
        await db.commit()
        await db.refresh(entity)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def user_registration(
        db,
        username: str,
        email: str,
        password_hash: str,
        first_name: str,
        last_name: str) -> str:

    try:
        role = "user"
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role
        )

        await save_entity(db, user)
        return str(user.id)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def check_user_exists(db, email: str, username: str) -> bool:
    query = select(User).where((User.username == username) | (User.email == email))
    result = await db.execute(query)
    user = result.scalars().first()
    return user is not None


async def get_user_by_username(db, username: str):
    query = select(User).filter(User.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def assing_team(
        db,
        user_id: str,
        team_id: str,
) -> None:
    try:
        userteamrole = UserTeamRole(
            user_id=user_id,
            team_id=team_id,
            role="owner"
        )

        await save_entity(db, userteamrole)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    

async def register_invitation(
        db,
        sender_id: str,
        recipient_id: str,
        team_id: str
) -> None:
    user_teams = await get_user_teams(db, sender_id)
    uuid_team_id = UUID(team_id)
    if uuid_team_id not in user_teams:
        raise HTTPException(status_code=401, detail="You don't have permission get this team.")
    try:
        status = "pendiente"
        invitation = Invitation(
            sender_id=sender_id,
            recipient_id=recipient_id,
            team_id=team_id,
            status=status
        )

        await save_entity(db, invitation)
    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))


async def update_invitation_status(
    db, 
    user_id: str,
    invitation_id: str, 
    status: str
) -> None:
    if status not in ["aceptado", "declinado"]:
        raise HTTPException(status_code=400, detail="Invalid status value.")
    
    uuid_invitation_id = UUID(invitation_id)

    try:
        # Buscar la invitación
        result = await db.execute(
            select(Invitation).where(Invitation.id == uuid_invitation_id)
        )
        invitation = result.scalar_one_or_none()
        
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitation not found.")
        
        # Actualizar estado y fechas
        invitation.status = status
        if status == "aceptado":
            invitation.accepted_at = datetime.utcnow()
        elif status == "declinado":
            invitation.rejected_at = datetime.utcnow()
        
        # Guardar cambios
        await db.commit()

    except SQLAlchemyError as sqlex:
        raise HTTPException(status_code=400, detail=str(sqlex))
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))
