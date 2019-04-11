from celery import Celery
from workerATasks import WorkerATasks
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)
# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'

# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(acks_late=True)
def long_task(name):
    task_id = long_task.request.id
    logger.info(f'Input: {name}')
    return WorkerATasks.long_task(name, task_id)


@celery.task()
def fail_task():
    return WorkerATasks.fail_task()
