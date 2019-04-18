import signal, os
from celery import Celery
from jobs.workerBJobs import WorkerBJobs
from kombu import Connection, Producer, Queue
import logging

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'

# Initialize Celery
celery = Celery('workerB', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Kombu Connection to message broker
kombuConnection = Connection('amqp://rabbitmq:rabbitmq@rabbit:5672//')

# Initialization of Producer
producer = Producer(kombuConnection, auto_declare=True)


# Kombu error callback
def errback(exc, interval):
    logging.error('Error: %r', exc, exc_info=1)
    logging.error('Retries in second', interval)


# Ensuring broker Connection
publish = kombuConnection.ensure(producer, producer.publish, errback=errback, max_retries=3)

workerBjobs = WorkerBJobs(publish)


@celery.task()
def counter_task():
    # Handling External SIGTERM to communicate with external python module
    signal.signal(signal.SIGTERM, workerBjobs.exit_gracefully)

    # Queue declaration for this task
    logs_queue = Queue(counter_task.request.id, routing_key=counter_task.request.id)

    # Calling external python module & passing message publisher
    result = workerBjobs.counter_task(logs_queue)
    if not result:
        publish({'Message': {'value': 'Exiting Gracefully'}}, routing_key=logs_queue.routing_key, declare=[logs_queue])
        raise Exception("Exiting from here ")


@celery.task()
def addition_task():
    # Queue declaration for this task
    logs_queue = Queue(addition_task.request.id, routing_key=addition_task.request.id)
    return workerBjobs.sum_task(logs_queue)
