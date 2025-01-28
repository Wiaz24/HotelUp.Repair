from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Enum as SqlEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as SqlUUID
from datetime import datetime
from schemas.enums import RepairType, TaskStatus
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.task_model import Task
from models.base_model import Base

class Janitor(Base):
    __tablename__ = "janitors"
    __table_args__ = {'schema': 'repair'}
    
    id = Column(SqlUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="janitor")