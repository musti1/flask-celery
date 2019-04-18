from celery import Celery, states
from subprocess import Popen, PIPE, STDOUT
import shlex
from kombu import Connection, Producer, Queue
import logging

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'

# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

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


@celery.task(acks_late=True)
def long_task(name):
    logs_queue = Queue(long_task.request.id, routing_key=long_task.request.id)
    # Sending Message back to broker
    publish({'Message': 'Executing Long Task'}, routing_key=logs_queue.routing_key,
            declare=[logs_queue])

    cmd = "sh jobs/longTaskjob.sh {}".format(name)
    process = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        # Sending Message back to broker
        publish({'Message': {'Current_value': line.decode(), 'task_id': logs_queue.routing_key}},
                routing_key=logs_queue.routing_key,
                declare=[logs_queue])


@celery.task()
def fail_task():
    logs_queue = Queue(fail_task.request.id, routing_key=fail_task.request.id)
    cmd = "sh jobs/failTaskjob.sh"
    # Sending Message back to broker
    publish({'Message': 'Executing Counter Task'}, routing_key=logs_queue.routing_key,
            declare=[logs_queue])

    process = Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=STDOUT, bufsize=0)
    line = process.stdout.readline()

    # Sending Message back to broker
    publish({'Message': {'Current_value': line.decode(), 'task_id': logs_queue.routing_key}},
            routing_key=logs_queue.routing_key,
            declare=[logs_queue])
    raise Exception(F'Task is failing')
