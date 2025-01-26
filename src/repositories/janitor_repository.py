from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import func # type: ignore
from models.task_model import Task
from models.janitor_model import Janitor
from typing import List
from datetime import datetime
from schemas.task import TaskCreate, TaskDelete, TaskUpdate
from schemas.enums import RepairType
from rabbitmq.rabbitmq_producer import send_message   

class JanitorRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_janitor_tasks(self, janitor_id: str) -> List[Task]:
        return self.db.query(Task).filter(Task.janitor_id == janitor_id).all()

    def get_janitor_with_least_tasks(self) -> Janitor:
        return self.session.query(Janitor).outerjoin(Task).group_by(Janitor.id).order_by(func.count(Task.id)).first()