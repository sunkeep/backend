import itertools
from flask import Flask
from flask import request
import MySQLdb
import string
import secret
import datetime
import json
import tasks

app = Flask(__name__)

db = MySQLdb.connect(host='95.46.99.185', user='mysql_user', passwd='MyNewPass', db='nasa_db', charset='utf8')
# db = MySQLdb.connect(host=secret.host, user=secret.user, passwd=secret.passwd, db=secret.db, charset='utf8')
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
    data = dictfetchall(cursor)
    res = json.dumps(data)
    return res

@app.route('/sundata', methods= ['GET'])
def get_sundata_by_timestamp():
    timestamp = request.args.get('timestamp')
    return timestamp


# TODO get current weather (Temperature | Pressure | Humidity | Solar radiation | Cloudiness | Sunrise / sunset | Wind speed | wind direction)
@app.route('/monitoring/current', methods=['GET'])
def get_current_monitoring_data():
    last_timestamp_exists = 1483264501
    res = get_monitoring_data(last_timestamp_exists)
    return res

@app.route('/panel/weather', methods=['GET'])
def get_weather():
    timestamp = request.args.get('timestamp')
    if timestamp is None:
        timestamp = 1475243723
    sql = "SELECT * FROM nasa_db.nasa_humidity WHERE `timestamp` = %d" % int(timestamp)
    cursor.execute(sql)
    data = dictfetchall(cursor)
    res = json.dumps(data)
    return res


def get_sunrise_time_by_timestamp(timestamp):
    sql = """SELECT nasa_sunrise.value as sunrise_at FROM nasa_sunrise WHERE timestamp = %d""" % timestamp
    cursor.execute(sql)
    sunrise = dictfetchall(cursor)
    sunrise[0]['sunrise_at'] = sunrise[0]['sunrise_at'][:1] + ':' + sunrise[0]['sunrise_at'][1:] + ':00'
    return sunrise


def get_sunset_time_by_timestamp(timestamp):
    sql = """SELECT nasa_sunset.value as sunset_at FROM nasa_sunset WHERE timestamp = %d""" % timestamp
    cursor.execute(sql)
    sunset = dictfetchall(cursor)
    sunset[0]['sunset_at'] = sunset[0]['sunset_at'][:2] + ':' + sunset[0]['sunset_at'][2:] + ':00'
    return sunset

# TODO Move it monitoring results
@app.route('/sunstatus', methods=['GET'])
def get_sun_status_by_timestamp():
    timestamp = request.args.get('timestamp')
    if timestamp is None:
        timestamp = 1483178400
    data = get_sunrise_time_by_timestamp(timestamp)[0]
    data.update(get_sunset_time_by_timestamp(timestamp)[0])
    # TODO Caulculate daytime left based on current time and sunset_at from data
    res = json.dumps(data)
    return res


if __name__ == '__main__':
    app.run(host='127.0.0.1')