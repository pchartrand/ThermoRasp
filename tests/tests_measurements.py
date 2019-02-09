from unittest import TestCase
from thermostat.measurements import Measurements


class MeasurementsTests(TestCase):
    def test_can_add_a_measurement(self):
        m = Measurements(10)
        m.add(dict(time=1, value=10.0))
        m.add(dict(time=2, value=11.0))

        self.assertEqual(2, m.len())


    def test_can_constrain_measurement_array(self):
        m = Measurements(2)
        m.add(dict(time=1, value=10.0))
        m.add(dict(time=2, value=11.0))
        m.add(dict(time=3, value=12.0))

        self.assertEqual(2, m.len())
        self.assertEqual(dict(time=2,value=11.0), m.measurements[0])


    def test_can_iterate_on_measurements(self):
        m1 = dict(time=1, value=10.0)
        m2 = dict(time=2, value=11.0)
        m3 = dict(time=3, value=12.0)

        m = Measurements(3)
        m.add(m1)
        m.add(m2)
        m.add(m3)

        measurements = []
        for measurement in m:
            measurements.append(measurement)

        self.assertEqual(measurements[0], m1)
        self.assertEqual(measurements[1], m2)
        self.assertEqual(measurements[2], m3)