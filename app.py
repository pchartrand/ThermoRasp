#!/usr/bin/env python3
import json
from flask import Flask, render_template, request, url_for, redirect
from scheduling.timeseries import series_to_json
from scheduling.timeutils import now, time_to_seconds
from scheduling.week import Week
from thermostat.temperature_controller import TemperatureController
from thermostat.measurements import Measurements




INITIAL_TARGET_TEMPERATURE = 20
HYSTERESIS = 0.5
ADC_GPIO_PIN = 6
RELAY_GPIO_PIN = 17
INITIAL_SCHEDULE_FILE = 'schedule.yml'
MAX_HISTORY = 2 * 24 * 7
previous_measurements = Measurements(MAX_HISTORY)

tc = TemperatureController(
    INITIAL_TARGET_TEMPERATURE,
    HYSTERESIS,
    ADC_GPIO_PIN,
    RELAY_GPIO_PIN,
    INITIAL_SCHEDULE_FILE
)

def round(val):
    return "{:.1f}".format(val)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_schedule():
    return render_template(
        'schedule.html',
        schedule=tc.schedule,
        date_time=time_to_seconds(),
        target=round(tc.target_temperature),
        heating=tc.heating,
        temperature=round(tc.current_temperature),
        automatic=tc.automatic
    )


@app.route('/status', methods=['GET'])
def show_status():
    return app.response_class(
        response=json.dumps(
            {"target": round(tc.target_temperature),
             "heating": tc.heating,
             "temperature": round(tc.current_temperature),
             "automatic": tc.automatic
             }
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/target', methods=['GET'])
def show_target():
    return app.response_class(
        response=json.dumps({"target": round(tc.target_temperature)}),
        status=200,
        mimetype='application/json'
    )


@app.route('/target', methods=['PUT'])
def set_target():
    temperature = request.json.get('target', tc.thermostat.target)
    tc.target_temperature = float(temperature)
    return redirect(url_for('show_target'))


@app.route('/heating', methods=['GET'])
def show_heating():
    return app.response_class(
        response=json.dumps(
            {"heating": tc.heating}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/heating', methods=['POST'])
def check():
    tc.check()
    return redirect(url_for('show_status'))


@app.route('/store', methods=['POST'])
def store_temperature():
    previous_measurements.add((now(), tc.current_temperature))
    return redirect(url_for('show_status'))


@app.route('/temperature', methods=['GET'])
def show_temperature():
    return app.response_class(
        response=json.dumps(
            {"temperature":  round(tc.current_temperature)}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/automatic', methods=['GET'])
def automatic():
    return app.response_class(
        response=json.dumps(
            {"automatic": tc.automatic}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/automatic', methods=['POST'])
def set_to_automatic():
    tc.automatic = True
    tc.check()
    return redirect(url_for('show_status'))

@app.route('/manual', methods=['GET'])
def manual():
    return app.response_class(
        response=json.dumps(
            {"manual": not tc.automatic}
        ),
        status=200,
        mimetype='application/json'
    )


@app.route('/manual', methods=['POST'])
def set_to_manual():
    tc.automatic = False
    tc.check()
    return redirect(url_for('show_status'))


@app.route('/schedule', methods=['GET'])
def send_schedule():
    serie = []
    week = Week()
    for day in tc.schedule_days:
        for time, event in tc.schedule_day_events(day):
            dt = week.event_time_in_week(day, event)
            prior = week.minute_prior_to_event(day, event)
            serie.append((prior, tc.scheduled_temperature_for(prior)))
            serie.append((dt, event.temperature))

    series_as_json = series_to_json([serie, previous_measurements])

    return app.response_class(
        response=json.dumps(series_as_json),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        tc.cleanup()