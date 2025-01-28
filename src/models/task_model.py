from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Enum as SqlEnum # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.dialects.postgresql import UUID as SqlUUID # type: ignore
from datetime import datetime
from schemas.enums import RepairType, TaskStatus # type: ignore
from sqlalchemy import ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from models.base_model import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'schema': 'repair'}
    
    id = Column(SqlUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    reservation_id = Column(SqlUUID(as_uuid=True), nullable=False)
    room_number = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = Column(DateTime)
    repair_type = Column(String(100), nullable=False, default="undefined")
    status = Column(String(100), nullable=False, default="pending")
    damage_repair_cost = Column(Float, nullable=False, default=0.0)
    janitor_id = Column(SqlUUID(as_uuid=True), ForeignKey('repair.janitors.id'))
    janitor = relationship("Janitor", back_populates="tasks")
    
    