class Thermostat(object):
    def __init__(self, target, hysteresis=0.5):
        self.target = target
        self.hysteresis = hysteresis
        self.heating = False

    def heat(self, temperature):
        if self.heating:
            target = self.target + self.hysteresis
            self.heating = False if temperature > target else True
        else:
            target = self.target - self.hysteresis
            self.heating = True if temperature < target else False
        return self.heating