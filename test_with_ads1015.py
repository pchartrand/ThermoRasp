#!/usr/bin/python3
# -*- coding:utf-8 -*-
from gpiozero import LED
from datetime import datetime as dt

from time import sleep
from thermostat.adc.tlc1453 import gpio_setup, gpio_cleanup
from thermostat.adc.ads1015 import ADS
from thermostat.termostat import Thermostat
from thermostat.ntc import convert_volts_to_temperature, convert_value_to_temperature
from thermostat.relay import LED


if __name__ == '__main__':
    gpio_setup()
    led = LED(17)
    try:
        adc = ADS()
        thermostat  = Thermostat(20, 0.5)
        while True:
            value = adc.read()
            volts = adc.read_volts()
            temperature = convert_value_to_temperature(value)

            heating = thermostat.check(temperature)
            heat = 'heating' if heating else ''
            if heating:
                led.on()
            else:
                led.off()
            print("{:%Y %m %d %H:%M:%S} {:04d} {:.2f} {:.2f} {}".format(dt.now(), value, volts, temperature, heat))
            sleep(1)

    finally:
        gpio_cleanup()

