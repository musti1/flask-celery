import signal, os
from celery import Celery
from jobs.workerBJobs import WorkerBJobs
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

workerBjobs = WorkerBJobs(logger)


@celery.task()
def counter_task():
    signal.signal(signal.SIGTERM, workerBjobs.exit_gracefully)
    result = workerBjobs.counter_task()
    if not result:
        raise Exception("Exiting from here ")


@celery.task()
def addition_task():
    return workerBjobs.sum_task()
