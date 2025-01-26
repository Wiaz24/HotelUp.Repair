from repositories.task_repository import TaskRepository
from models.task_model import Task
from typing import List

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def get_all_tasks(self) -> List[Task]:
        return self.task_repository.get_all_tasks()
    
    def create_task(self, task_data):
        task = self.task_repository.create_task(task_data)
        janitor = self.task_repository.get_janitor_with_least_tasks()
        task.janitor_id = janitor.id
        self.task_repository.update_task({'id': task.id, 'janitor_id': janitor.id})
        return task
    
    def update_task(self, task_data):
        return self.task_repository.update_task(task_data)
    
    def delete_task(self, task_id):
        return self.task_repository.delete_task(task_id)
    
class JanitorService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def get_janitor_tasks(self, janitor_id: str) -> List[Task]:
        return self.task_repository.get_janitor_tasks(janitor_id)