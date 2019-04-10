from celery import Celery
from workerBTask import WorkerBTasks

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@localhost:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerB', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task()
def counter_task():
    return WorkerBTasks.counter_task()


@celery.task()
def addition_task():
    return WorkerBTasks.sum_task()
