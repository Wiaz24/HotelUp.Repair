from pydantic import BaseModel, Field # type: ignore
from datetime import datetime
from typing import List, Optional
from schemas.enums import RepairType, TaskStatus
from enum import Enum
from uuid import UUID
from schemas.task import TaskBase
   
class Janitor(BaseModel):
    janitor_id: UUID
    tasks: List[TaskBase]

class Config:
    from_attributes = True