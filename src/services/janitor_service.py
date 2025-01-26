from repositories.task_repository import TaskRepository
from models.task_model import Task
from typing import List

class JanitorService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def get_janitor_tasks(self, janitor_id: str) -> List[Task]:
        return self.task_repository.get_janitor_tasks(janitor_id)