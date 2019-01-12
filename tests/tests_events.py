from unittest import TestCase
from scheduling.schedule import Event


class EventTests(TestCase):
    def test_can_create_an_event(self):
        event = Event(8, 30, 17)
        assert event.temperature == 17
        assert event.minute == 30
        assert event.hour == 8
        assert event.minutes == 510
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

    def test_can_get_event_time_as_hour_minutes(self):
        event = Event(2, 30, 25)

        event_time = event.get_time()

        assert event_time == '02:30', event_time

    def test_can_change_event_time_using_time_as_hour_minutes(self):
        event = Event(0, 0, 25)

        event.set_time('15:30')

        assert event.get_time() == '15:30'

    def test_event_can_be_created_with_time_as_hour_minutes(self):
        event = Event.set('5:45', '20')
        assert event.hour == 5
        assert event.minute == 45
        assert event.temperature == 20