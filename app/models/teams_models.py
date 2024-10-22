from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as GUID
from sqlalchemy.orm import relationship
import uuid
from app.models.base import Base
from datetime import datetime


class Team(Base):
    __tablename__ = 'teams'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_roles = relationship("UserTeamRole", back_populates="team")