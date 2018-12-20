from unittest import TestCase
from thermostat.termostat import Thermostat


class TermostatTests(TestCase):
    def test_can_check_a_temperature_that_raises(self):
        t = Thermostat(20,0.5)

        heating = t.check(19)

        self.assertTrue(heating)

        heating = t.check(19.5)

        self.assertTrue(heating)

        heating = t.check(20)

        self.assertTrue(heating)

        heating = t.check(20.5)

        self.assertTrue(heating)

        heating = t.check(21)

        self.assertFalse(heating)

    def test_can_check_a_temperature_that_falls(self):
        t = Thermostat(20,0.5)

        heating = t.check(21)

        self.assertFalse(heating)

        heating = t.check(20.5)

        self.assertFalse(heating)

        heating = t.check(20)

        self.assertFalse(heating)

        heating = t.check(19.5)

        self.assertFalse(heating)

        heating = t.check(19)

        self.assertTrue(heating)

    def test_can_set_a_target(self):
        t = Thermostat(20, 0.5)

        heating = t.check(19)

        self.assertTrue(heating)

        heating = t.set_target(17)

        self.assertFalse(heating)