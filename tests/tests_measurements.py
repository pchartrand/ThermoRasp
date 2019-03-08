from unittest import TestCase
from thermostat.measurements import Measurements
import datetime


class NextMinuteIterator(object):
    def __init__(self):
        self.now = datetime.datetime.now()

    def __iter__(self):
        return self

    def next(self):
        now = self.now
        self.now += datetime.timedelta(minutes=1)
        return now


class MeasurementsTests(TestCase):
    def test_can_add_a_measurement(self):
        di = NextMinuteIterator()
        m = Measurements(10)
        m.add((di.next(), 10.0))
        m.add((di.next(), 11.0))

        self.assertEqual(2, len(m))


    def test_can_constrain_measurement_array(self):
        di = NextMinuteIterator()
        d1 = di.next()
        d2 = di.next()
        d3 = di.next()
        m = Measurements(2)
        m.add((d1, 10.0))
        m.add((d2, 11.0))
        m.add((d3, 12.0))

        self.assertEqual(2, len(m))
        self.assertEqual((d2,11.0), m.measurements[0])


    def test_can_iterate_on_measurements(self):
        di = NextMinuteIterator()
        d1 = di.next()
        d2 = di.next()
        d3 = di.next()
        m1 = (d1, 10.0)
        m2 = (d2, 11.0)
        m3 = (d3, 12.0)

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

    def test_can_remove_old_values(self):

        now = datetime.datetime.now()
        m = Measurements(5)
        monday = m.week_start()
        m1 = (monday - datetime.timedelta(days=1), 10)
        m2 = (monday, 11)
        m3 = (monday +  datetime.timedelta(hours=1), 12)
        m4 = (now, 13)
        m5 = (now + datetime.timedelta(days=5), 14)

        m.add(m1)
        m.add(m2)
        m.add(m3)
        m.add(m4)
        m.add(m5)

        self.assertEqual(3, len(m))

        measurements = []
        for measurement in m:
            measurements.append(measurement)

        self.assertEqual(measurements[0], m3)
        self.assertEqual(measurements[1], m4)
        self.assertEqual(measurements[2], m5)