from celery import Celery,states
from celery.exceptions import Ignore
from workerATasks import WorkerATasks
import celstash
import logging

#Celstash Initialization
celstash.configure(logstash_host='logstash', logstash_port=9999)
logger = celstash.new_logger('flask-celery')
logger.setLevel(logging.INFO)
# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'

# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(acks_late=True)
def long_task(name):
    task_id = long_task.request.id
    return WorkerATasks.long_task(logger, name, task_id)


@celery.task()
def fail_task():
    return WorkerATasks.fail_task(logger)
    raise Ignore()
