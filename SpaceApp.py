from flask import Flask
from flask import request
import MySQLdb
import string
import secret

app = Flask(__name__)

db = MySQLdb.connect(host=secret.host, user=secret.user, passwd=secret.passwd, db=secret.db, charset='utf8')
cursor = db.cursor()


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!@'

@app.route('/panels/status', methods=['GET'])
def get_panel_statuses():
    sql = "SELECT * FROM nasa_sunrise"
    cursor.execute(sql)
    data = cursor.fetchall()
    return '{statuses:[]}'

@app.route('/panels/status/<int:panel_id>', methods=['GET'])
def get_panel_status(panel_id):
    return '{status:{%d}}' % panel_id

@app.route('/panels/data', methods=['GET'])
def get_panel_datas():
    return '{datas:[]}'

@app.route('/panels/data/<int:panel_id>', methods=['GET'])
def get_panel_data(panel_id):
    return '{data:{%d}}' % panel_id

@app.route('/panels/add', methods=['POST'])
def add_panel():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        sql = ""
        cursor.execute(sql)
        db.commit()
        db.close()
        return name
    else:
        return "error"


if __name__ == '__main__':
    app.run(host='95.46.99.185')
