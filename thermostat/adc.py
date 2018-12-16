from time import sleep

import RPi.GPIO as GPIO


def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(True)


def gpio_cleanup():
    GPIO.cleanup()


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
