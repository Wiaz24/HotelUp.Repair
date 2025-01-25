from fastapi import FastAPI # type: ignore
from routers import task_router
from database.database import engine
from models.task import Base
import sys
import threading
from rabbitmq.rabbitmq_consumer import start_consumer
from sqlalchemy.exc import OperationalError # type: ignore
from sqlalchemy import inspect # type: ignore

print(sys.path)
app = FastAPI()

# # Create database tables
# Base.metadata.create_all(bind=engine)
# Check if the database and tables exist
def check_and_create_tables():
    inspector = inspect(engine)
    if not inspector.has_table("tasks", schema="repair"):
        Base.metadata.create_all(bind=engine)

# Create database tables if they do not exist
check_and_create_tables()

# Include routers
app.include_router(task_router.router)

# Start RabbitMQ consumer
@app.on_event("startup")
def startup_event():
    start_consumer()