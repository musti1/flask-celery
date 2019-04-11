from workerA import long_task, fail_task
from workerB import counter_task, addition_task
from flowerApi import FlowerApi
from EsHelper import EsHelper
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
    return render_template('pages/logs.html', logs=logs)


@app.route('/execute_task', methods=['GET'])
def execute_long_task():
    task_name = request.args.get('task_name')
    if task_name == 'long':
        name = request.args.get('name')
        long_task.delay(name)
    elif task_name == 'counter':
        counter_task.delay()
    elif task_name == 'addition':
        addition_task.delay()
    elif task_name == 'fail':
        fail_task.delay()

    return jsonify({}), 200


@app.route('/tasks', methods=['GET'])
def get_tasks():
    FlowerApi.list_tasks()
    return jsonify({}), 200


@app.route('/terminate', methods=['GET'])
def terminate():
    task_id = request.args.get('task_id')
    FlowerApi.terminate(task_id)
    return jsonify({}), 200


if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
