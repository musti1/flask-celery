from workerA import long_task
from workerB import counter_task, addition_task
from flowerApi import FlowerApi
from EsHelper import EsHelper
from flask import (
    Flask,
    request,
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
    if task_name == 'longtask':
        name = request.args.get('name')
        long_task.delay(name)
    elif task_name == 'counter':
        counter_task.delay()
    elif task_name == 'addition':
        addition_task.delay()
    return redirect(url_for('home'))


@app.route('/terminate', methods=['GET'])
def terminate():
    task_id = request.args.get('task_id')
    FlowerApi.terminate(task_id)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
