import signal, os
from celery import Celery
from jobs.workerBJobs import WorkerBJobs
import celstash
from kombu import Connection, Producer, Queue
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
    logs_queue = Queue(counter_task.request.id, routing_key=counter_task.request.id)
    kombuConnection = Connection('amqp://rabbitmq:rabbitmq@rabbit:5672//')
    producer = Producer(kombuConnection, auto_declare=True)
    publish = kombuConnection.ensure(producer, producer.publish, errback=errback, max_retries=3)
    result = workerBjobs.counter_task(publish, logs_queue)
    if not result:
        publish({'Exception': 'Exiting Gracefully'}, routing_key=logs_queue.routing_key, declare=[logs_queue])
        raise Exception("Exiting from here ")


@celery.task()
def addition_task():
    return workerBjobs.sum_task()


def errback(exc, interval):
    logger.error('Error: %r', exc, exc_info=1)
    logger.error('retiers in second', interval)
