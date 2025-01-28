from http.client import HTTPException
from repositories.janitor_repository import JanitorRepository
from models.task_model import Task
from schemas.janitor import JanitorResponse
from typing import List, Optional
from uuid import UUID

class JanitorService:
    def __init__(self, janitor_repository: JanitorRepository):
        self.janitor_repository = janitor_repository

    def get_tasks_by_janitor_id(self, janitor_id: UUID):
        return self.janitor_repository.get_tasks_by_janitor_id(janitor_id)

    def create_janitor(self, janitor_data):
        return self.janitor_repository.create_janitor(janitor_data)
    
    def get_janitor_list(self):
        return self.janitor_repository.get_janitor_list()
    