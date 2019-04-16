#!/usr/local/bin/python3
from queue import Empty
from time import sleep
from kombu import Connection , Queue
from workerA import long_task, fail_task
from workerB import counter_task, addition_task
from flowerApi import FlowerApi
from EsHelper import EsHelper
from flask_socketio import SocketIO, emit
from flask import (
    Flask,
    request,
    jsonify,
    render_template,
    redirect, url_for
)

app = Flask(__name__)
app.debug = True
app.clients = {}
esHelper = EsHelper()
socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template('pages/controlPanel.html')


@app.route("/logs")
def show_logs():
    task_id = request.args.get('task_id')
    result = esHelper.fetch(task_id)
    logs = []
    for hit in result['hits']['hits']:
        logs.append(hit['_source'].to_dict())
    return jsonify(logs)

@app.route("/updated_logs")
def get_updated_logs():
    task_id = request.args.get('task_id')
    date_from = request.args.get('date_from')
    result = esHelper.fetchUpdatedLogs(task_id,date_from)
    logs = []
    for hit in result['hits']['hits']:
        logs.append(hit['_source'].to_dict())
    return jsonify(logs)


@app.route('/execute_task', methods=['GET'])
def execute_long_task():
    task_name = request.args.get('task_name')
    if task_name == 'long':
        name = request.args.get('name')
        long_task.apply_async(args=[name],queue='workerA')
    elif task_name == 'counter':
        counter_task.apply_async(queue='workerB')
    elif task_name == 'addition':
        addition_task.apply_async(queue='workerB')
    elif task_name == 'fail':
        fail_task.apply_async(queue='workerA')

    return jsonify({}), 200


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = FlowerApi.list_tasks()
    return jsonify(task_list), 200

@app.route('/workers', methods=['GET'])
def get_workers():
    worker_list = FlowerApi.list_workers()
    return jsonify(worker_list), 200

@app.route('/terminate', methods=['GET'])
def terminate():
    task_id = request.args.get('task_id')
    FlowerApi.terminate(task_id)
    return jsonify({}), 200

@socketio.on('getLogs',namespace='/test')
def test_message(data):
    with Connection('amqp://rabbitmq:rabbitmq@rabbit:5672/') as _conn:
        sub_queue = _conn.SimpleQueue(str(data['task_id']))
        while True:
            try:
                _msg = sub_queue.get(block=False)
                emit('response_to_web',str(_msg.payload))
                _msg.ack()
                sleep(0.5)
            except Empty:
                break
        sub_queue.close()
        chan = _conn.channel()
        dq = Queue(name=str(data['task_id']),exchange="")
        bdq = dq(chan)
        bdq.delete()



if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
