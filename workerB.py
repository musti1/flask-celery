from celery import Celery
from workerBTask import WorkerBTasks
import celstash
import logging

celstash.configure(logstash_host='logstash', logstash_port=9999)
logger = celstash.new_logger('flask-celery')
logger.setLevel(logging.INFO)
# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerB', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task()
def counter_task():
    return WorkerBTasks.counter_task(logger)


@celery.task()
def addition_task():
    return WorkerBTasks.sum_task(logger)
