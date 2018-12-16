#!/usr/bin/env python
import json
from flask import Flask, render_template, request, make_response, url_for, redirect
from thermostat.ntc import convert_to_temperature
from thermostat.adc import TLC, gpio_setup, gpio_cleanup
from thermostat.termostat import Thermostat
from thermostat.relay import Relay

gpio_setup()
relay = Relay(17)
adc = TLC(6)
thermostat = Thermostat(20, 0.5)
app = Flask(__name__)


def get_target():
    return "{:.1f}".format(thermostat.target)


def get_temperature():
    return "{:.1f}".format(convert_to_temperature(adc.read()))


def get_heating():
    return thermostat.heating


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


@app.route('/', methods=['GET'])
def show_status():
    return app.response_class(
        response=json.dumps(
            {"target": get_target(), "heating": get_heating(), "temperature": get_temperature()}
        ),
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