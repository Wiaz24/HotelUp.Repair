from pydantic import BaseModel, Field # type: ignore
from datetime import datetime
from typing import List, Optional
from schemas.enums import RepairType, TaskStatus
from enum import Enum
from uuid import UUID
from schemas.task import TaskBase
   
class JanitorBase(BaseModel):
    id: UUID
    tasks: List[TaskBase] = []
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class JanitorCreate(BaseModel):
    id: UUID
    email: str
    role: str

    class Config:
        from_attributes = True
        
class JanitorResponse(BaseModel):
    id: UUID
    tasks: List[TaskBase] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True