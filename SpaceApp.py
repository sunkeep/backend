from flask import Flask
from flask import request
import MySQLdb
import string
import secret
import json

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
    res = json.dumps(data)
    return res

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


# TODO get current weather (Temperature | Pressure | Humidity | Solar radiation | Cloudiness | Sunrise / sunset | Wind speed | wind direction)
@app.route('/panel/weather', methods=['GET'])
def get_weather():
    # sql = "SELECT * FROM nasa_db.nasa_humidity WHERE `timestamp` < 1473010221"
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # res = json.dumps(data)
    # return res
    error = None
    if request.method == 'GET':
        name = request.form['timestamp']
        sql = "SELECT * FROM nasa_db.nasa_humidity WHERE `timestamp` < %d" % name
        cursor.execute(sql)
        data = cursor.fetchall()
        res = json.dumps(data)
        return res
    else:
        return "error"


# TODO get today sun status

if __name__ == '__main__':
    app.run(host='95.46.99.185')
