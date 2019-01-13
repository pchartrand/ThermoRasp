#!/usr/bin/env python
import json
from flask import Flask, render_template, request, url_for, redirect
from scheduling.timeseries import series_to_json
from scheduling.timeutils import time_to_seconds
from scheduling.week import Week
from temperature_controller import TemperatureController


INITIAL_TARGET_TEMPERATURE = 20
HYSTERESIS = 0.5
ADC_GPIO_PIN = 6
RELAY_GPIO_PIN = 17
INITIAL_SCHEDULE_FILE = 'schedule.yml'

tc = TemperatureController(
    INITIAL_TARGET_TEMPERATURE,
    HYSTERESIS,
    ADC_GPIO_PIN,
    RELAY_GPIO_PIN,
    INITIAL_SCHEDULE_FILE
)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_schedule():
    tc.set_target_from_schedule()
    return render_template('schedule.html', schedule=tc.schedule, date_time=time_to_seconds())


@app.route('/status', methods=['GET'])
def show_status():
    return app.response_class(
        response=json.dumps(
            {"target": tc.get_formatted_target(),
             "heating": tc.is_heating(),
             "temperature": tc.get_formatted_temperature()
             }
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/target', methods=['GET'])
def show_target():
    return app.response_class(
        response=json.dumps({"target": tc.get_formatted_target()}),
        status=200,
        mimetype='application/json'
    )


@app.route('/target', methods=['PUT'])
def set_target():
    temperature = request.json.get('target', tc.thermostat.target)
    tc.set_target_temperature(float(temperature))
    return redirect(url_for('show_target'))


@app.route('/heating', methods=['GET'])
def show_heating():
    return app.response_class(
        response=json.dumps(
            {"heating": tc.is_heating()}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/heating', methods=['POST'])
def check():
    #tc.set_target_from_schedule()
    if tc.should_heat():
        tc.start_heating()
    else:
        tc.stop_heating()
    return redirect(url_for('show_status'))


@app.route('/temperature', methods=['GET'])
def show_temperature():
    return app.response_class(
        response=json.dumps(
            {"temperature": tc.get_formatted_temperature()}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/schedule', methods=['GET'])
def send_schedule():
    serie = []
    current = []
    week = Week()
    for day in tc.schedule_days():
        for time, event in tc.schedule_day_events(day):
            dt = week.event_time_in_week(day, event)
            prior = week.minute_prior_to_event(day, event)
            serie.append((prior, tc.get_scheduled_temperature_for(prior)))
            serie.append((dt, event.temperature))
    series_as_json = series_to_json([serie, current])

    return app.response_class(
        response=json.dumps(series_as_json),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        tc.gpio_cleanup()