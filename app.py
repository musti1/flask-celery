from workerA import long_task
from workerB import counter_task
from flask import (
    Flask,
    jsonify,
    request,
    render_template
)

app = Flask(__name__)
app.debug = True
app.clients = {}


@app.route("/")
def home():
    return render_template('pages/controlPanel.html')


@app.route('/longtask', methods=['GET'])
def execute_long_task():
    name = request.args.get('name')
    task = long_task.delay(name)
    return jsonify({}), 202


@app.route('/counter', methods=['GET'])
def execute_counter_task():
    task = counter_task.delay()
    return jsonify({}), 202


if __name__ == '__main__':
    app.run(debug=True)
