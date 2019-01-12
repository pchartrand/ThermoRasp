class Event(object):

    @staticmethod
    def _check_time(hour, minute):
        assert 0 <= hour < 24
        assert 0 <= minute < 60

    @staticmethod
    def _check_temperature(temperature):
        assert 5 <= temperature < 26

    @staticmethod
    def set(time, temperature):
        hour, minute = time.split(':')
        return Event(int(hour), int(minute), int(temperature))

    def __init__(self, hour, minute, temperature):
        Event._check_time(hour, minute)
        self.hour = hour
        self.minute = minute
        self._set_minutes()
        Event._check_temperature(temperature)
        self.temperature = temperature

    def _set_minutes(self):
        self.minutes = 60*self.hour + self.minute

    def get_time(self):
        return "%02d:%02d" % (self.hour, self.minute)

    def set_time(self, time):
        hour, minute = time.split(':')
        self._check_time(int(hour), int(minute))
        self.hour = int(hour)
        self.minute = int(minute)
        self._set_minutes()

    def is_before(self, minutes, previous_event):
        assert isinstance(previous_event, Event)
        return bool(previous_event.minutes <= minutes < self.minutes)