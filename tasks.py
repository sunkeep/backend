from flask import Flask
from flask import request

app = Flask(__name__)


# TODO implement
@app.route('/tasks/add', methods=['POST'])
def task_add():
    return "true"


# TODO implement
@app.route('/tasks/check', methods=['GET'])
def task_check():
    return "true"


# TODO implement
@app.route('/tasks/all', methods=['GET'])
def task_get_all():
    return "true"


# TODO implement
def task_pause(task_id):
    return "true"


# TODO implement
def task_resume(task_id):
    return "true"


# TODO implement
def task_category_pause(category_id):
    return "true"


# TODO implement
def task_category_resume(category_id):
    return "true"
