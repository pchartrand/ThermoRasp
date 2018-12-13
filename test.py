#!/usr/bin/python3
# -*- coding:utf-8 -*-
from gpiozero import LED
from datetime import datetime as dt

from thermostat.tlc import TLC, GPIO
from thermostat.termostat import Thermostat
from thermostat.ntc import convert_to_temperature


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)
    led = LED(17)
    try:
        adc = TLC(6)
        thermostat  = Thermostat(20, 0.5)
        while True:
            value = adc.read()
            temperature = convert_to_temperature(value)
            heating = thermostat.check(temperature)
            heat = 'heating' if heating else ''
            if heating:
                led.on()
            else:
                led.off()
            print("{:%Y %m %d %H:%M:%S} {:04d} {:.1f} {}".format(dt.now(), value, temperature, heat))
            #sleep(1)

    finally:
        GPIO.cleanup()

