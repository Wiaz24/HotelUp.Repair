from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.database import get_db

router = APIRouter(
    prefix="/api/repair",
    tags=["Health"]
)

@router.get("/_health")
def health_check():
    return {"status": "ok"}

@router.get("/db_health")
def db_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        print("Error 503: Service Unavailable")
        return {"error": f"Could not connect to database: {str(e)}"}, 503
    # ... existing code ...

@router.post("/truncate_db")
def truncate_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("TRUNCATE TABLE repair.tasks"))
        return {"status": "ok"}
    except Exception as e:
        print("Error 500: Internal Server Error")
        return {"error": f"Internal server error: {str(e)}"}, 500