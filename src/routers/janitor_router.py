from fastapi import APIRouter, Depends, Form, HTTPException
from typing import Annotated, List
from sqlalchemy.orm import Session
from database.database import get_db
from services.janitor_service import JanitorService
from repositories.janitor_repository import JanitorRepository
from schemas.janitor import JanitorCreate, JanitorBase, JanitorResponse
from schemas.task import TaskResponse

router = APIRouter(
    prefix="/api/repair",
    tags=["Janitors"]
)

@router.get("/janitors/{janitor_id}/tasks", response_model=JanitorResponse)
def get_tasks_by_janitor_id(janitor_id: str, db: Session = Depends(get_db)):
    try:
        janitor_repository = JanitorRepository(db)
        janitor_service = JanitorService(janitor_repository)
        return janitor_service.get_tasks_by_janitor_id(janitor_id)
    except ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to database"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid value: {str(e)}"
        )
    except RecursionError:
        raise HTTPException(
            status_code=500,
            detail="Internal server error: maximum recursion depth exceeded"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/janitors", response_model=JanitorCreate)
def create_janitor(janitor: Annotated[JanitorCreate, Form()], db: Session = Depends(get_db)):
    try:
        janitor_repository = JanitorRepository(db)
        janitor_service = JanitorService(janitor_repository)
        return janitor_service.create_janitor(janitor)
    except ConnectionError:
        print("Error 503: Service Unavailable")
        return {"error": "Could not connect to database"}, 503
    except ValueError as e:
        print("Error 400: Bad Request")
        return {"error": f"Invalid value: {str(e)}"}, 400
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500

@router.get("/janitors", response_model=List[JanitorBase])
def get_janitor_list(db: Session = Depends(get_db)):
    try:
        janitor_repository = JanitorRepository(db)
        janitor_service = JanitorService(janitor_repository)
        return janitor_service.get_janitor_list()
    except ConnectionError:
        print("Error 503: Service Unavailable")
        return {"error": "Could not connect to database"}, 503
    except ValueError as e:
        print("Error 400: Bad Request")
        return {"error": f"Invalid value: {str(e)}"}, 400
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500
    