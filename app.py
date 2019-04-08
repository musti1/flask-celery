from celery import Celery
from workerATasks import WorkerATasks
from flask import (
    Flask,
    jsonify,
    request
)

app = Flask(__name__)
app.debug = True
app.clients = {}
app.config['SECRET_KEY'] = 'top-secret!'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'amqp://rabbitmq:rabbitmq@localhost:5672/'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)


@celery.task(bind=True)
def long_task(self, name):
    task_id = self.request.id
    tasks = WorkerATasks()
    return tasks.execute(name, task_id)


@app.route('/longtask', methods=['GET'])
def longtask():
    name = request.args.get('name')
    task = long_task.delay(name)
    return jsonify({}), 202


if __name__ == '__main__':
    app.run(debug=True)
