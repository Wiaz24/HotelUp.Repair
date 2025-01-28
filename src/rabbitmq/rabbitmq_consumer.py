from datetime import datetime
import json
import pika # type: ignore
import threading
from services.task_service import TaskService
from services.janitor_service import JanitorService
from repositories.task_repository import TaskRepository
from repositories.janitor_repository import JanitorRepository
from database.database import get_db
from schemas.task import TaskCreate
from schemas.janitor import JanitorCreate
from uuid import UUID
from env import settings

# Initialize TaskService
db = get_db()
task_repository = TaskRepository(db)
janitor_repository = JanitorRepository(db)
janitor_service = JanitorService(janitor_repository)
task_service = TaskService(task_repository, janitor_repository)


def callback(ch, method, properties, body):
    exchange = method.exchange
    print(f"Received task from {exchange}: {body}")
    
    if exchange == 'HotelUp.Customer:ReservationCreatedEvent':
        create_task_event(body)
    elif exchange == 'HotelUp.Customer:ReservationCanceledEvent':
        delete_task_event(body)
    elif exchange == 'HotelUp.Employee:UserCreatedEvent':
        create_janitor(body)
        
def create_task_event(body):
    message = json.loads(body)['message']
    reservation_id = message['reservationId']
    start_date = datetime.strptime(message['startDate'], '%Y-%m-%dT%H:%M:%SZ').date()
    rooms = message['rooms']
    
    db = next(get_db())
    task_repository = TaskRepository(db)
    janitor_repository = JanitorRepository(db)
    task_service = TaskService(task_repository, janitor_repository)
        
    for room in rooms:
        task_for_room = TaskCreate(
            title='Cyclic room check task',
            reservation_id=reservation_id,
            description='Check the room for any damages and report them',
            room_number=room['id'],
            deadline=start_date
        )
        task_service.create_task(task_for_room)


def delete_task_event(body):
    message = json.loads(body)['message']
    reservation_id = message['reservationId']
    db = next(get_db())
    task_repository = TaskRepository(db)
    janitor_repository = JanitorRepository(db)
    task_service = TaskService(task_repository, janitor_repository)
    task_service.delete_task(reservation_id)
    
def create_janitor(body):
    message = json.loads(body)['message']
    janitor_id = UUID(message['employeeId'])
    janitor_email = message['employeeEmail']
    role = message['role']
    
    if role != 'janitor':
        return
    
    janitor = JanitorCreate(id=janitor_id, email=janitor_email, role=role)
    db = next(get_db())
    janitor_repository = JanitorRepository(db)
    janitor_service = JanitorService(janitor_repository)
    print(f"Creating janitor: {janitor}")
    janitor_service.create_janitor(janitor)
    
def consume():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=5672))
        print("Connection established successfully.")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to establish connection: {e}")
        return

    channel = connection.channel()
    
    # Declare the exchanges
    exchange_names = ['HotelUp.Customer:ReservationCreatedEvent', 'HotelUp.Customer:ReservationCanceledEvent', 'HotelUp.Employee:UserCreatedEvent']
    for exchange_name in exchange_names:
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout', durable=True)
        print(f"Declared exchange {exchange_name}")
    
    # Declare the queue
    queue_name = 'HotelUp.RepairTask:Queue'
    channel.queue_declare(queue=queue_name, durable=True)
    
    # Bind the queue to each exchange
    for exchange_name in exchange_names:
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        print(f"Bound queue {queue_name} to exchange {exchange_name}")
    
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print('Waiting for tasks. To exit press CTRL+C')
    channel.start_consuming()

def start_consumer():
    thread = threading.Thread(target=consume)
    thread.start()