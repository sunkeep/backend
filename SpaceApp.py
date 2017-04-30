import itertools
from flask import Flask
from flask import request
import MySQLdb
import string
import secret
import json
import time
import datetime

# import tasks

app = Flask(__name__)

db = MySQLdb.connect(host=secret.host, user=secret.user, passwd=secret.passwd, db=secret.db, charset='utf8')
cursor = db.cursor()


def dictfetchall(curs):
    desc = curs.description
    return [dict(itertools.izip([col[0] for col in desc], row))
            for row in curs.fetchall()]


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


# TODO Add sunrise\sunset and Cloudiness
# and kill my self for this code.
def get_monitoring_data(timestamp):
    sql = """SELECT  `nasa_humidity`.`value` AS humidity,
            `nasa_barometric_pressure`.`value` AS barometric_pressure,
            `nasa_solar_radiation`.`value` AS solar_radiation,
            `nasa_temperature`.`value` AS temperature,
            `nasa_wind_direction`.`value` AS wind_direction,
            `nasa_wind_speed`.`value` AS wind_speed
    FROM nasa_humidity
    INNER JOIN nasa_barometric_pressure ON nasa_humidity.timestamp=nasa_barometric_pressure.timestamp
    INNER JOIN nasa_solar_radiation ON nasa_humidity.timestamp=nasa_solar_radiation.timestamp
    INNER JOIN nasa_temperature ON nasa_humidity.timestamp=nasa_temperature.timestamp
    INNER JOIN nasa_wind_direction ON nasa_humidity.timestamp=nasa_wind_direction.timestamp
    INNER JOIN nasa_wind_speed ON nasa_humidity.timestamp=nasa_wind_speed.timestamp
    WHERE `nasa_humidity`.timestamp=%d""" % timestamp
    cursor.execute(sql)
    data = dictfetchall(cursor)
    res = json.dumps(data)
    return res


# TODO get current weather (Temperature | Pressure | Humidity | Solar radiation | Cloudiness | Sunrise / sunset | Wind speed | wind direction)
@app.route('/monitoring/current', methods=['GET'])
def get_current_monitoring_data():
    last_timestamp_exists = 1475243723
    res = get_monitoring_data(last_timestamp_exists)
    return res


@app.route('/panel/weather', methods=['GET'])
def get_weather():
    # sql = "SELECT * FROM nasa_db.nasa_humidity WHERE `timestamp` < 1473010221"
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # res = json.dumps(data)
    # return res
    error = None
    if request.method == 'GET':
        timestamp = request.args.get('timestamp')
        sql = "SELECT * FROM nasa_db.nasa_humidity WHERE `timestamp` = %d" % int(timestamp)
        cursor.execute(sql)
        data = dictfetchall(cursor)
        res = json.dumps(data)
        return res
    else:
        return "error"


# @app.route('/panels/weather/<int:timestamp>', methods=['GET'])
# def get_weather(timestamp):
#     error = None
#     if request.method == 'GET':
#         sql = "SELECT `value` FROM nasa_db.nasa_humidity WHERE `timestamp` < %d" % timestamp
#         cursor.execute(sql)
#         data = dictfetchall(cursor)
#         res = json.dumps(data)
#         return res
#     else:
#         return "error"


# TODO get today sun status
def get_today_sun_status():
    return True


@app.route('/sensor/value/add', methods=['POST'])
def add_sensor_data():
    error = None
    if request.method == 'POST':
        json = request.json
        temperature = json['temperature']
        pressure = json['pressure']
        light = json['light']
        ts = time.time()
        dateValue = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeValue = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        timestamp = str(int(ts))
        insert_to_db(
            "INSERT INTO nasa_db.real_pressure (timestamp, date, time, value, text) VALUES ('" + timestamp + "', '" + dateValue + "', '" + timeValue + "', '" + pressure + "', null);")
        insert_to_db(
            "INSERT INTO nasa_db.real_temperature (timestamp, date, time, value, text) VALUES ('" + timestamp + "', '" + dateValue + "', '" + timeValue + "', '" + temperature + "', null);")
        insert_to_db(
            "INSERT INTO nasa_db.real_light (timestamp, date, time, value, text) VALUES ('" + timestamp + "', '" + dateValue + "', '" + timeValue + "', '" + light + "', null);")
        db.close()
        return "saved"
    else:
        return "error"


def insert_to_db(sqlPressure):
    cursor.execute(sqlPressure)
    db.commit()


def get_sun_status_by_timestamp(timestamp):
    # TODO 1: Convert timestamp to YYYY-MM-DD
    # TODO 2: Get sunrise timestamp and calc passed sunday amount.
    # TODO 3: Get sunset timestamp and calc e
    return True


if __name__ == '__main__':
    app.run(host='95.46.99.185',debug=True)
