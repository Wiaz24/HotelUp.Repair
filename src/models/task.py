from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Enum as SqlEnum # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from datetime import datetime
from schemas.enums import RepairType, TaskStatus # type: ignore

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {'schema': 'repair'}
    
    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, nullable=False)
    room_number = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    repair_type = Column(String(100), nullable=False, default="undefined")
    status = Column(String(100), nullable=False, default="pending")
    demage_repair_cost = Column(Float, nullable=False, default=0.0)
