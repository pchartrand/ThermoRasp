# requires Adafruit_Blinka and python3

import board
import busio
import adafruit_ads1x15.ads1015 as _ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS(object):
    def __init__(self, channel=_ADS.P0):
        i2c = busio.I2C(board.SCL, board.SDA)
        ads = _ADS.ADS1015(i2c)
        self.chan = AnalogIn(ads, channel)

    def read(self):
        return self.chan.value

    def read_volts(self):
        return self.chan.voltage