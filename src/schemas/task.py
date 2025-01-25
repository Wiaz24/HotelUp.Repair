from pydantic import BaseModel, Field # type: ignore
from datetime import datetime
from typing import Optional
from schemas.enums import RepairType, TaskStatus
from enum import Enum

class RepairType(str, Enum):
    undefined = "undefined"
    demage = "demage"
    malfunction = "malfunction"
    not_detected = "not_detected"

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"

class TaskBase(BaseModel):
    id: int
    reservation_id: int
    created_at: datetime
    last_updated: datetime  
    repair_type: RepairType
    status: TaskStatus
    description: Optional[str] = None
    room_number: int
    demage_repair_cost: float
    title: str
  
class TaskCreate(BaseModel):
    title: str
    reservation_id: int
    description: Optional[str] = None
    room_number: int

class TaskUpdate(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    demage_repair_cost: float
    repair_type: RepairType
    

class TaskResponse(BaseModel):
    id: int
    reservation_id: int
    created_at: datetime
    last_updated: datetime  
    repair_type: RepairType
    status: TaskStatus
    description: Optional[str] = None
    room_number: int
    demage_repair_cost: float
    title: str
    
class Config:
    from_attributes = True