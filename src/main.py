from fastapi import FastAPI # type: ignore
from routers import task_router, janitor_router, health_router
from database.database import engine
from models.task_model import Base
import sys
import threading
from rabbitmq.rabbitmq_consumer import start_consumer
from sqlalchemy.exc import OperationalError # type: ignore
from sqlalchemy import inspect # type: ignore

print(sys.path)
app = FastAPI(
    title="HotelUp Repair Service",
    description="API for managing hotel repairs and maintenance")

app.include_router(task_router.router)
app.include_router(janitor_router.router)
app.include_router(health_router.router)

# # Create database tables
# Base.metadata.create_all(bind=engine)
# Check if the database and tables exist
def check_and_create_tables():
    inspector = inspect(engine)
    if not inspector.has_table("tasks", schema="repair"):
        Base.metadata.create_all(bind=engine)

# Create database tables if they do not exist
check_and_create_tables()

# Start RabbitMQ consumer
@app.on_event("startup")
def startup_event():
    start_consumer()