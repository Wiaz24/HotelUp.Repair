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

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://cognito-idp.us-east-1.amazonaws.com/us-east-1_Y15zULckX/.well-known/openid-configuration")

SECRET_KEY = "dummysecret"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="/api/repair",
    tags=["Tasks"],
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Task related routes
@router.get("/api/repair/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    try:
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
    
@router.post("/api/repair/tasks", response_model=TaskCreate)
def create_task(task: Annotated[TaskCreate, Form()], db: Session = Depends(get_db)):
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

@router.put("/api/repair/tasks/{task_id}", response_model=TaskUpdate)
def update_task(task_id: str, task: Annotated[TaskUpdate, Form()], db: Session = Depends(get_db)):
    try:
        task_repository = TaskRepository(db)
        janitor_repository = JanitorRepository(db)
        task_service = TaskService(task_repository, janitor_repository)
        result = task_service.update_task(task)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return result
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to database")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/api/repair/tasks/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    try:
        task_repository = TaskRepository(db)
        janitor_repository = JanitorRepository(db)
        task_service = TaskService(task_repository, janitor_repository)
        result = task_service.delete_task(task_id)
        if not result:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"status": "ok"}
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Could not connect to database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/tasks/unassigned", response_model=List[TaskResponse])
def get_unassigned_tasks(db: Session = Depends(get_db)):
    task_repository = TaskRepository(db)
    return task_repository.get_unassigned_tasks()

@router.put("/tasks/{task_id}/claim", response_model=TaskResponse, tags=["Tasks"])
def claim_task(task_id: str, janitor_id: str, db: Session = Depends(get_db)):
    task_repository = TaskRepository(db)
    return task_repository.claim_task(janitor_id, task_id)