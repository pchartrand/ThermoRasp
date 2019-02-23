import datetime

class Measurements(object):
    def __init__(self, max):
        self.MAX = max
        self.measurements = []

    @staticmethod
    def week_start():
        current_time = datetime.datetime.now()
        return current_time - datetime.timedelta(
            hours=current_time.hour,
            minutes=current_time.minute,
            days=current_time.weekday()
        )

    def delete_last_week(self):
        monday = self.week_start()
        for measurement in self.measurements[:]:
            if measurement['time'] < monday:
                self.measurements.remove(measurement)

    def add(self, measurement):
        self.delete_last_week()
        self.measurements.append(measurement)
        self.trim()

    def __len__(self):
        return len(self.measurements)

    def trim(self):
        l = len(self)
        if l > self.MAX:
            self.measurements = self.measurements[l - self.MAX:]

    def __iter__(self):
        for measurement in self.measurements:
            yield measurement