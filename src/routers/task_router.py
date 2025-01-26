from typing import Annotated, List
from fastapi import APIRouter, Depends, Form, HTTPException, status # type: ignore
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import text # type: ignore
from database.database import get_db
from services.task_service import TaskService
from services.janitor_service import JanitorService
from repositories.janitor_repository import JanitorRepository
from repositories.task_repository import TaskRepository
from schemas.task import RepairType, TaskBase, TaskCreate, TaskResponse, TaskUpdate
from schemas.janitor import JanitorCreate, JanitorBase, JanitorResponse
from jose import JWTError, jwt
from open_id_connect import requires_role

router = APIRouter()

router = APIRouter(
    prefix="/api/repair",
    tags=["Tasks"],
)


# Task related routes
@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    user: dict = Depends(requires_role(["Admins", "Janitors"]))
):
    try:
        if "Admins" in user.get("roles", []):
            tasks = task_service.get_all_tasks()
        else:
            janitor_id = user["sub"]  # Extract janitor ID from token
            if not janitor_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not extract janitor ID from token"
                )
            
        task_repository = TaskRepository(db)
        janitor_repository = JanitorRepository(db)
        task_service = TaskService(task_repository, janitor_repository)
        tasks = task_service.get_all_tasks()
        return [TaskResponse.from_orm(task) for task in tasks]
    except ConnectionError:
        print("Error 503: Service Unavailable")
        return {"error": "Could not connect to database"}, 503
    except ValueError as e:
        print("Error 400: Bad Request")
        return {"error": f"Invalid value: {str(e)}"}, 400
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500
    
@router.post("/tasks", response_model=TaskCreate)
def create_task(
    task: Annotated[TaskCreate, Form()],
    db: Session = Depends(get_db),
    user: dict = Depends(requires_role(["Admins", "Receptionists"]))
):
    try:          
        task_repository = TaskRepository(db)
        janitor_repository = JanitorRepository(db)
        task_service = TaskService(task_repository, janitor_repository)
        result = task_service.create_task(task)
        return result
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to database")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/tasks/", response_model=TaskUpdate)
def update_task(
    task: Annotated[TaskUpdate, Form()], 
    db: Session = Depends(get_db),
    user: dict = Depends(requires_role(["Admins", "Janitors"]))
):
    try:
        if "Admins" in user.get("roles", []):
            result = task_service.update_task(task, None)
        else:
            janitor_id = user["sub"]  # Extract janitor ID from token
            if not janitor_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not extract janitor ID from token"
                )
                
        task_repository = TaskRepository(db)
        janitor_repository = JanitorRepository(db)
        task_service = TaskService(task_repository, janitor_repository)
        result = task_service.update_task(task, janitor_id)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return result
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to database")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.delete("/tasks/{task_id}")
# def delete_task(task_id: str, db: Session = Depends(get_db)):
#     try:
#         task_repository = TaskRepository(db)
#         janitor_repository = JanitorRepository(db)
#         task_service = TaskService(task_repository, janitor_repository)
#         result = task_service.delete_task(task_id)
#         if not result:
#             raise HTTPException(status_code=404, detail="Task not found")
#         return {"status": "ok"}
#     except ConnectionError:
#         raise HTTPException(status_code=503, detail="Could not connect to database")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tasks/unassigned", response_model=List[TaskResponse])
def get_unassigned_tasks(
    db: Session = Depends(get_db),
    user: dict = Depends(requires_role(["Admins", "Janitors"]))
):
    try:
        if "Admins" in user.get("roles", []):
            return task_repository.get_unassigned_tasks()
        else:
            janitor_id = user["sub"]  # Extract janitor ID from token
            if not janitor_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not extract janitor ID from token"
                )
                
            task_repository = TaskRepository(db)
            return task_repository.get_unassigned_tasks()
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}/claim", response_model=TaskResponse, tags=["Tasks"])
def claim_task(
    task_id: str, 
    db: Session = Depends(get_db),
    user: dict = Depends(requires_role(["Admins", "Janitors"]))
):
    try:
        if "Admins" in user.get("roles", []):
            return task_repository.claim_task(None, task_id)
        else:
            janitor_id = user["sub"]  # Extract janitor ID from token
            if not janitor_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Could not extract janitor ID from token"
                )
                
            task_repository = TaskRepository(db)
            return task_repository.claim_task(janitor_id, task_id)
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))