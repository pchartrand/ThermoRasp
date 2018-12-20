from unittest import TestCase
from scheduling.schedule import Event


class EventTests(TestCase):
    def test_can_create_an_event(self):
        event = Event(8, 30, 17)
        assert event.temperature == 17
        assert event.minute == 30
        assert event.hour == 8
        assert event.get_time() == '08:30'

    def test_event_hour_is_valid(self):
        try:
            Event(25, 30, 17)
            raise Exception("should have raised an assertion error")
        except AssertionError:
            pass

    def test_event_minute_is_valid(self):
        try:
            Event(5, 60, 17)
            raise Exception("should have raised an assertion error")
        except AssertionError:
            pass

    def test_event_temperature_is_not_to_high(self):
        try:
            Event(5, 30, 26)
            raise Exception("should have raised an assertion error")
        except AssertionError:
            pass

    def test_event_temperature_is_not_too_low(self):
        try:
            Event(5, 30, 4)
            raise Exception("should have raised an assertion error")
        except AssertionError:
            pass