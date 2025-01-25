from sqlalchemy.orm import Session # type: ignore
from models.task import Task
from typing import List
from datetime import datetime
from schemas.task import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all_tasks(self) -> List[Task]:
        return self.db.query(Task).all()
    
    def create_task(self, task_data: TaskCreate):
        task_dict = task_data.dict()
        current_time = datetime.utcnow()
        task = Task(**task_dict, created_at=current_time, last_updated=current_time)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
    
    def update_task(self, task_data: TaskUpdate):
        task = self.db.query(Task).filter(Task.id == task_data.id).first()
        if task:
            update_data = task_data.dict()
            for key, value in update_data.items():
                setattr(task, key, value)
            task.last_updated = datetime.utcnow()  # Update last_updated field
            self.db.commit()
            self.db.refresh(task)
            return task
        return None
    
    def delete_task(self, task_id):
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            self.db.delete(task)
            self.db.commit()
            return task
        return None