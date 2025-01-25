from fastapi import FastAPI # type: ignore
from routers import task_router
from database.database import engine
from models.task import Base
import sys
import threading
from rabbitmq_consumer import start_consumer

print(sys.path)
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(task_router.router)

# Start RabbitMQ consumer
@app.on_event("startup")
def startup_event():
    start_consumer()