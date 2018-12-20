from unittest import TestCase
from thermostat.ntc import convert_to_temperature


class TemperatureConversionTests(TestCase):
    def test_can_convert_digital_values_to_temperatures(self):
        self.assertEqual(10.0, round(10*convert_to_temperature(250)/10))
        self.assertEqual(15.0, round(10 * convert_to_temperature(280) / 10))
        self.assertEqual(20.0, round(10 * convert_to_temperature(320) / 10))
        self.assertEqual(25.0, round(10 * convert_to_temperature(365) / 10))