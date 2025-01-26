from enum import Enum
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Enum as SqlEnum # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.dialects.postgresql import UUID as SqlUUID # type: ignore
from datetime import datetime
from schemas.enums import RepairType, TaskStatus # type: ignore
from sqlalchemy import ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from models.task_model import Base


class Janitor(Base):
    __tablename__ = "janitors"
    __table_args__ = {'schema': 'repair'}
    
    id = Column(SqlUUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    tasks = relationship("Task", back_populates="janitor")