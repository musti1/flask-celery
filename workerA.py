from celery import Celery
from workerATasks import WorkerATasks


# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'

# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task()
def long_task(name):
    task_id = long_task.request.id
    return WorkerATasks.long_task(name, task_id)


@celery.task()
def fail_task():
    return WorkerATasks.fail_task()
