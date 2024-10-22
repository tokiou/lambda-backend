# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as GUID
import uuid
from app.models.teams_models import Team
from app.models.content_models import NoteColumns, Note, Idea, Project
from app.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, nullable=False)

    team_roles = relationship("UserTeamRole", back_populates="user")
    user_quotas = relationship("UserQuota", back_populates="user")

class UserTeamRole(Base):
    __tablename__ = 'users_teamrole'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(GUID(), ForeignKey('users.id'), nullable=False)
    team_id = Column(GUID(), ForeignKey('teams.id'), nullable=False)
    role = Column(String, nullable=False)
    signed_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="team_roles")
    team = relationship("Team", back_populates="user_roles")

class UserQuota(Base):
    __tablename__ = 'users_quota'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(GUID(), ForeignKey('users.id'), nullable=False)
    quota = Column(Integer, default=100)
    last_quota_charge = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="user_quotas")


class Invitation(Base):
    __tablename__ = 'invitations'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    sender_id = Column(GUID(), ForeignKey('users.id'), nullable=False)
    recipient_id = Column(GUID(), ForeignKey('users.id'), nullable=False)
    team_id = Column(GUID(), ForeignKey('teams.id'), nullable=False)
    status = Column(String, nullable=False, default='pending')  # 'pending', 'accepted', 'rejected'
    sent_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)

    sender = relationship("User", foreign_keys=[sender_id])
    recipient = relationship("User", foreign_keys=[recipient_id])
    team = relationship("Team")
