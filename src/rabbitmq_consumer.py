import pika # type: ignore
import threading

def callback(ch, method, properties, body):
    print(f"Received task: {body}")
    # Process the task here

def consume():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
        print("Connection established successfully.")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to establish connection: {e}")
        return

    channel = connection.channel()
    channel.queue_declare(queue='RepairTaskQueue', durable=True)
    channel.basic_consume(queue='task_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for tasks. To exit press CTRL+C')
    channel.start_consuming()

def start_consumer():
    thread = threading.Thread(target=consume)
    thread.start()