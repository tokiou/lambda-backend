from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as GUID
import uuid
from datetime import datetime
from app.models.teams_models import Team


class Idea(Base):
    __tablename__ = 'ideas'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    idea = Column(Text, nullable=True)
    project_id = Column(GUID(), ForeignKey('projects.id'), nullable=True)
    user_id = Column(GUID(), ForeignKey('users.id'), nullable=False)
    status = Column(String, nullable=False)
    team_id = Column(GUID(), ForeignKey('teams.id'), nullable=False)
    priority = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Note(Base):
    __tablename__ = 'notes'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    note = Column(Text, nullable=True)
    user_id = Column(GUID(), ForeignKey('users.id'), nullable=False)
    status = Column(String, nullable=False)
    column_id = Column(GUID(), ForeignKey('notes_columns.id'), nullable=False)
    priority = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    column = relationship("NoteColumns", back_populates="notes")

class NoteColumns(Base):
    __tablename__ = 'notes_columns'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    team_id = Column(GUID(), ForeignKey('teams.id'), nullable=False)
    name = Column(String, nullable=False)
    project_id = Column(GUID(), ForeignKey('projects.id'), nullable=True)
    priority = Column(Integer, nullable=False)
    status = Column(String, nullable=False)

    notes = relationship("Note", back_populates="column")

class Project(Base):
    __tablename__ = 'projects'

    id = Column(GUID(), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    team_id = Column(GUID(), ForeignKey('teams.id'), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)