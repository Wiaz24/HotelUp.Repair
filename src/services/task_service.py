from repositories.task_repository import TaskRepository
from models.task import Task
from typing import List

class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def get_all_tasks(self) -> List[Task]:
        return self.task_repository.get_all_tasks()
    
    def create_task(self, task_data):
        return self.task_repository.create_task(task_data)
    
    def update_task(self, task_data):
        return self.task_repository.update_task(task_data)
    
    def delete_task(self, task_id):
        return self.task_repository.delete_task(task_id)