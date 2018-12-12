#!/usr/bin/env python
from gpiozero import LED
import json
from flask import Flask, render_template, request, make_response, url_for, redirect
from thermostat.ntc import convert_to_temperature
from thermostat.tlc import TLC, GPIO
from thermostat.termostat import Thermostat

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
led = LED(17)
adc = TLC(6)
thermostat = Thermostat(20, 0.5)
app = Flask(__name__)


@app.route('/', methods=['GET'])
def status():
    target = "{:.1f}".format(thermostat.target)
    temperature = "{:.1f}".format(convert_to_temperature(adc.read()))
    response = app.response_class(
        response=json.dumps(
            {"target": target, "heating": thermostat.heating, "temperature": temperature}
        ),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/target', methods=['GET'])
def get_target():
    value = "{:.1f}".format(thermostat.target)
    response = app.response_class(
        response=json.dumps({"target": value}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/target', methods=['PUT'])
def set_target():
    temperature = request.json.get('target')
    thermostat.set_target(float(temperature))
    return redirect(url_for('get_target'))


@app.route('/heating', methods=['POST'])
def heating():
    heating = thermostat.set(convert_to_temperature(adc.read()))
    if heating:
        led.on()
    else:
        led.off()
    response = app.response_class(
        response=json.dumps({"heating": heating}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/temperature', methods=['GET'])
def get_temperature():
    temperature = "{:.1f}".format(convert_to_temperature(adc.read()))
    response = app.response_class(
        response=json.dumps(
            {"temperature": temperature}
        ),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        GPIO.cleanup()