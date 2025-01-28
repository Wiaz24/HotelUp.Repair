from pydantic import BaseModel, Field # type: ignore
from datetime import datetime
from typing import Optional
from schemas.enums import RepairType, TaskStatus
from enum import Enum
from uuid import UUID
   
class TaskBase(BaseModel):
    id: UUID
    reservation_id: UUID
    created_at: datetime
    last_updated: datetime  
    repair_type: RepairType
    status: TaskStatus
    description: Optional[str] = None
    room_number: int
    damage_repair_cost: float
    title: str
    deadline: datetime
    janitor_id: Optional[UUID] = None
    class Config:
        from_attributes = True
  
class TaskCreate(BaseModel):
    title: str
    reservation_id: UUID
    description: Optional[str] = None
    room_number: int
    deadline: datetime

class TaskUpdate(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus
    damage_repair_cost: float
    repair_type: RepairType
    

class TaskResponse(BaseModel):
    id: UUID
    reservation_id: UUID
    created_at: datetime
    last_updated: datetime  
    repair_type: RepairType
    status: TaskStatus
    description: Optional[str] = None
    room_number: int
    damage_repair_cost: float
    title: str
    deadline: datetime
    janitor_id: Optional[UUID] = None
    
    class Config:
        orm_mode = True
        from_attributes = True
    
class TaskDelete(BaseModel):
    id: UUID
    
class Config:
    from_attributes = True