#!/usr/bin/env python
import datetime
import json
import os
from flask import Flask, render_template, request, make_response, url_for, redirect
from thermostat.ntc import convert_to_temperature
from thermostat.adc import TLC, gpio_setup, gpio_cleanup
from thermostat.termostat import Thermostat
from thermostat.relay import Relay
from scheduling.schedule import read_schedule


DATETIME_SECONDS = '%Y-%m-%d %H:%M:%S'
DATETIME_MINUTES = '%Y-%m-%d %H:%M'

gpio_setup()
relay = Relay(17)
adc = TLC(6)
thermostat = Thermostat(20, 0.5)
schedule = read_schedule(os.path.join(os.path.dirname(__file__), 'schedule.yml'))
app = Flask(__name__)


def get_target():
    return "{:.1f}".format(thermostat.target)


def get_temperature():
    return "{:.1f}".format(convert_to_temperature(adc.read()))


def get_heating():
    return thermostat.heating


def now():
    return datetime.datetime.now()+ datetime.timedelta(hours=-5)


def get_time():
    return now().strftime(DATETIME_SECONDS)


def series_to_json(series):
    as_json = []
    for n, serie  in enumerate(series):
        serie_as_json = []
        for point in serie:
            date_value = point[0].strftime(DATETIME_MINUTES)
            value = round(point[1], 1)
            serie_as_json.append(
                dict(
                    date=date_value,
                    value=value
                )
            )
        as_json.append(serie_as_json)
    return as_json


@app.route('/target', methods=['GET'])
def show_target():
    return app.response_class(
        response=json.dumps({"target": get_target()}),
        status=200,
        mimetype='application/json'
    )


@app.route('/heating', methods=['GET'])
def show_heating():
    return app.response_class(
        response=json.dumps(
            {"heating": get_heating()}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/temperature', methods=['GET'])
def show_temperature():
    return app.response_class(
        response=json.dumps(
            {"temperature": get_temperature()}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/status', methods=['GET'])
def show_status():
    return app.response_class(
        response=json.dumps(
            {"target": get_target(), "heating": get_heating(), "temperature": get_temperature()}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/', methods=['GET'])
def show_schedule():
    current_target_temperature = schedule.get_temperature_for(now())
    if current_target_temperature != thermostat.target:
        print("setting temperature to {}".format(current_target_temperature))
        thermostat.set_target(float(current_target_temperature))
    return render_template('schedule.html', schedule=schedule, date_time=get_time())


@app.route('/schedule-data.json', methods=['GET'])
def send_schedule():
    serie = []
    current = []
    now =  datetime.datetime.now()
    week_start = now - datetime.timedelta(hours=now.hour, minutes=now.minute,days=now.weekday())
    for day in schedule.schedule:
        for time, event in schedule.schedule[day].items():
            dt = week_start + datetime.timedelta(days=day,hours=event.hour,minutes=event.minute)
            serie.append((dt, event.temperature))
    series_as_json = series_to_json([serie,current])

    return app.response_class(
        response=json.dumps(series_as_json),
        status=200,
        mimetype='application/json'
    )

@app.route('/set', methods=['PUT'])
def set_target():
    temperature = request.json.get('target', thermostat.target)
    thermostat.set_target(float(temperature))
    return redirect(url_for('show_target'))


@app.route('/check', methods=['POST'])
def check():
    heating = thermostat.check(convert_to_temperature(adc.read()))
    if heating:
        relay.on()
    else:
        relay.off()
    return redirect(url_for('show_status'))


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        gpio_cleanup()