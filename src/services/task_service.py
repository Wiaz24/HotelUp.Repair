from repositories.task_repository import TaskRepository
from repositories.janitor_repository import JanitorRepository
from models.task_model import Task
from typing import List
from fastapi import HTTPException

class TaskService:
    def __init__(self, task_repository: TaskRepository, janitor_repository: JanitorRepository):
        if not task_repository or not janitor_repository:
            raise ValueError("Required repositories must be provided")
        self.task_repository = task_repository
        self.janitor_repository = janitor_repository
    
    def get_all_tasks(self) -> List[Task]:
        try:
            return self.task_repository.get_all_tasks()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    def create_task(self, task_data):
        # Find janitor with least tasks (may be None)
        janitor = self.janitor_repository.get_janitor_with_least_tasks()
        # Create task with optional janitor_id
        janitor_id = janitor.id if janitor else None
        return self.task_repository.create_task(task_data, janitor_id)
    
    def update_task(self, task_data, janitor_id):
        return self.task_repository.update_task(task_data, janitor_id)
           

    
    def delete_task(self, task_id):
        try:
            return self.task_repository.delete_task(task_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def get_unassigned_tasks(self):
        try:
            return self.task_repository.get_unassigned_tasks()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    def claim_task(self, janitor_id, task_id):
        try:
            return self.janitor_repository.claim_task(janitor_id, task_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))