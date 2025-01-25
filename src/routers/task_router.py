from typing import Annotated, List
from fastapi import APIRouter, Depends, Form # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import text # type: ignore
from database.database import get_db
from services.task_service import TaskService
from repositories.task_repository import TaskRepository
from schemas.task import RepairType, TaskBase, TaskCreate, TaskResponse, TaskUpdate

router = APIRouter()
# Tasl related routes
@router.get("/api/repair/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    try:
        task_repository = TaskRepository(db)
        task_service = TaskService(task_repository)
        return task_service.get_all_tasks()
    except ConnectionError:
        print("Error 503: Service Unavailable")
        return {"error": "Could not connect to database"}, 503
    except ValueError as e:
        print("Error 400: Bad Request")
        return {"error": f"Invalid value: {str(e)}"}, 400
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500
    
@router.post("/api/repair/tasks", response_model=TaskCreate)
def create_task(task: Annotated[TaskCreate, Form()], db: Session = Depends(get_db)):
    try:
        task_repository = TaskRepository(db)
        task_service = TaskService(task_repository)
        return task_service.create_task(task)
    except ConnectionError:
        print("Error 503: Service Unavailable")
        return {"error": "Could not connect to database"}, 503
    except ValueError as e:
        print("Error 400: Bad Request")
        return {"error": f"Invalid value: {str(e)}"}, 400
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500

@router.put("/api/repair/tasks/{task_id}", response_model=TaskUpdate)
def update_task(task: Annotated[TaskUpdate, Form()], db: Session = Depends(get_db)):
    try:
        task_repository = TaskRepository(db)
        task_service = TaskService(task_repository)
        return task_service.update_task(task)
    except ConnectionError:
        print("Error 503: Service Unavailable")
        return {"error": "Could not connect to database"}, 503
    except ValueError as e:
        print("Error 400: Bad Request")
        return {"error": f"Invalid value: {str(e)}"}, 400
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500

@router.delete("/api/repair/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    try:
        task_repository = TaskRepository(db)
        task = task_repository.delete_task(task_id)
        if task:
            return {"status": "ok"}
        else:
            print("Error 404: Not Found")
            return {"error": "Task not found"}, 404
    except ConnectionError:
        print("Error 503: Service Unavailable")
        return {"error": "Could not connect to database"}, 503
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500

# Health check routes
@router.get("/api/repair/_health")
def health_check():
    return {"status": "ok"}

@router.get("/api/repair/db_health")

@router.post("/api/repair/truncate_db")
def truncate_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("TRUNCATE TABLE repair.tasks"))
        return {"status": "ok"}
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500

def db_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        print("Error 503: Service Unavailable")
        return {"error": f"Could not connect to database: {str(e)}"}, 503
