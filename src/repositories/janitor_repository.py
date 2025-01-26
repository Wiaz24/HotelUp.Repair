from http.client import HTTPException
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func # type: ignore
from models.task_model import Task
from models.janitor_model import Janitor
from typing import List, Optional   
from schemas.janitor import JanitorCreate, JanitorResponse
from schemas.task import TaskBase

class JanitorRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_tasks_by_janitor_id(self, janitor_id: str) -> JanitorResponse:
        janitor = self.db.query(Janitor).filter(Janitor.id == janitor_id).first()
        if not janitor:
            raise HTTPException(status_code=404, detail="Janitor not found")
        # Initialize empty tasks list if None
        task_schemas = [TaskBase.from_orm(task) for task in (janitor.tasks or [])]
        return JanitorResponse(id=janitor.id, tasks=task_schemas)

    def get_janitor_with_least_tasks(self) -> Janitor:
        return self.db.query(Janitor)\
            .outerjoin(Task)\
            .group_by(Janitor.id)\
            .order_by(func.count(Task.id))\
            .first()
    
    def create_janitor(self, janitor: JanitorCreate):
        janitor = Janitor(**janitor.dict())
        self.db.add(janitor)
        self.db.commit()
        self.db.refresh(janitor)
        return janitor
    
    def get_janitor_list(self) -> List[Janitor]:
        return self.db.query(Janitor).all()
    