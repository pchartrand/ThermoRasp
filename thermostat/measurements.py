class Measurements(object):
    def __init__(self, max):
        self.MAX = max
        self.measurements = []

    def add(self, measurement):
        self.measurements.append(measurement)
        self.trim()

    def len(self):
        return len(self.measurements)

    def trim(self):
        l = self.len()
        if l > self.MAX:
            self.measurements = self.measurements[l - self.MAX:]

    def __iter__(self):
        for measurement in self.measurements:
            yield measurement