from datetime import datetime
import json
import pika # type: ignore
import threading
from services.task_service import TaskService
from repositories.task_repository import TaskRepository
from database.database import get_db
from schemas.task import TaskCreate

# Initialize TaskService
db = get_db()
task_repository = TaskRepository(db)
task_service = TaskService(task_repository)

def callback(ch, method, properties, body):
    exchange = method.exchange
    print(f"Received task from {exchange}: {body}")
    
    if exchange == 'HotelUp.Customer:ReservationCreatedEvent':
        create_task_event(body)
    elif exchange == 'HotelUp.Customer:ReservationCanceledEvent':
        delete_task_event(body)
        
def create_task_event(body):
    message = json.loads(body)['message']
    reservation_id = message['reservationId']
    start_date = datetime.strptime(message['startDate'], '%Y-%m-%dT%H:%M:%SZ').date()
    rooms = message['rooms']
    
    for room in rooms:
        task_for_room = TaskCreate(
            title='Cyclic room check task',
            reservation_id=reservation_id,
            description='Check the room for any damages and report them',
            room_number=room['id'],
            deadline=start_date
        )
        db = next(get_db())
        task_repository = TaskRepository(db)
        task_service = TaskService(task_repository)
        task_service.create_task(task_for_room)

def delete_task_event(body):
    message = json.loads(body)['message']
    reservation_id = message['reservationId']
    db = next(get_db())
    task_repository = TaskRepository(db)
    task_service = TaskService(task_repository)
    task_service.delete_task(reservation_id)
    
def consume():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        print("Connection established successfully.")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to establish connection: {e}")
        return

    channel = connection.channel()
    
    # Declare the exchanges
    exchange_names = ['HotelUp.Customer:ReservationCreatedEvent', 'HotelUp.Customer:ReservationCanceledEvent']
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