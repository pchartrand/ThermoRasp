#!/usr/bin/python3
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
from gpiozero import LED
from time import sleep
from datetime import datetime as dt


class TLC(object):
    CLOCK = 16
    ADDRESS = 20
    DATA_OUT = 21
    CS = 19
    SLEEPTIME = 0.000001

    def __init__(self, channel):
        GPIO.setup(self.CLOCK, GPIO.OUT)
        GPIO.setup(self.ADDRESS, GPIO.OUT)
        GPIO.setup(self.CS, GPIO.OUT)
        GPIO.setup(self.DATA_OUT, GPIO.IN, GPIO.PUD_UP)
        GPIO.output(self.CS, GPIO.HIGH)

        self.channel = channel
        self.data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def high(self):
        GPIO.output(self.CLOCK, GPIO.HIGH)

    def low(self):
        GPIO.output(self.CLOCK, GPIO.LOW)

    def cycle(self):
        self.high()
        sleep(self.SLEEPTIME)
        self.low()
        sleep(self.SLEEPTIME)

    def convert(self):
        return (512 if self.data[8] else 0) + (256 if self.data[9] else 0) \
           + (128 if self.data[0] else 0) + (64 if self.data[1]  else 0) \
           + (32 if self.data[2] else 0) + (16 if self.data[3] else 0) \
           + (8 if self.data[4] else 0) + (4 if self.data[5] else 0) \
           + (2 if self.data[6] else 0) + self.data[7]

    def adress(self, i):
        if ((self.channel >> (3 - i)) & 0x01):
            GPIO.output(self.ADDRESS, GPIO.HIGH)
        else:
            GPIO.output(self.ADDRESS, GPIO.LOW)

    def read(self):
        GPIO.output(self.CS, GPIO.LOW)
        self.cycle()
        self.cycle()
        for i in range(14):
            self.high()
            if i < 4:
                self.adress(i)
            if i < 10:
                self.data[i] = GPIO.input(self.DATA_OUT)
            if i == 10:
                GPIO.output(self.CS, GPIO.HIGH)
            sleep(self.SLEEPTIME)
            self.low()
            sleep(self.SLEEPTIME)
        return self.convert()


def convert_to_temperature(value):
    '''
    Assuming a third degree polynomial relationship between voltage
    and temperature with a voltage divider made of an ntc
    thermistor (pullup) and a 5k6 resistor (to ground).
    Voltage measured across the 5k6 resistor.
    '''
    REFERENCE_VOLTS = 5.04
    A = 3.296
    B = -22.378
    C = 70.951
    D = -49.382
    volts = (value / 1023.0) * REFERENCE_VOLTS;
    return A*volts**3 + B*volts**2 + C*volts + D


class Thermostat(object):
    def __init__(self, target, hysteresis=0.5):
        self.target = target
        self.hysteresis = hysteresis
        self.heating = False

    def heat(self, temperature):
        if self.heating:
            target = self.target + self.hysteresis
            self.heating = False if temperature > target else True
        else:
            target = self.target - self.hysteresis
            self.heating = True if temperature < target else False
        return self.heating


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
            heating = thermostat.heat(temperature)
            heat = 'heating' if heating else ''
            if heating:
                led.on()
            else:
                led.off()
            print("{:%Y %m %d %H:%M:%S} {:04d} {:.1f} {}".format(dt.now(), value, temperature, heat))
            #sleep(1)

    finally:
        GPIO.cleanup()

