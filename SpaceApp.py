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


#TODO Add sunrise\sunset and Cloudiness
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
    values = cursor.fetchall()
    data = {'humidity': float(values[0][0]), 'barometric_pressure': float(values[0][1]),
            'solar_radiation': float(values[0][2]), 'temperature': float(values[0][3]),
            'wind_direction': float(values[0][4]), 'wind_speed': float(values[0][5])}
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
        # name = request.form['timestamp']
        current_timestamp = 1475243723
        sql = "SELECT * FROM nasa_db.nasa_humidity WHERE `timestamp` = %d" % current_timestamp
        cursor.execute(sql)
        data = cursor.fetchall()
        res = json.dumps(data)
        return res
    else:
        return "error"


# TODO get today sun status



if __name__ == '__main__':
    app.run(host='127.0.0.1')
