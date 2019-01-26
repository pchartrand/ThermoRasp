import os

from scheduling.schedule import read_schedule
from scheduling.timeutils import now
from thermostat.adc.tlc1453 import gpio_setup, gpio_cleanup
from thermostat.adc.ads1015 import ADS
from thermostat.ntc import convert_value_to_temperature
from thermostat.relay import Relay
from thermostat.termostat import Thermostat


class TemperatureController(object):
    def __init__(self, target_temperature, hysteresis, adc_gpio_pin, relay_gpio_pin, schedule_file):
        self.setup()
        self.thermostat = Thermostat(target_temperature, hysteresis)
        self.adc = ADS()
        self.heater = Relay(relay_gpio_pin)
        self.schedule = read_schedule(os.path.join(os.path.dirname(__file__), schedule_file))
        self.automatic = True

    def setup(self):
        gpio_setup()

    def cleanup(self):
        gpio_cleanup()

    def check(self):
        if self.automatic:
            self.set_target_from_schedule()
        self.heating = True if self.should_heat() else False

    @property
    def target_temperature(self):
        return self.thermostat.target

    @target_temperature.setter
    def target_temperature(self, target_temperature):
        self.thermostat.set_target(target_temperature)

    @property
    def current_temperature(self):
        return convert_value_to_temperature(self.adc.read())

    def current_temperature_formatted(self):
        return "{:.1f}".format(self.current_temperature)

    @property
    def heating(self):
        return self.thermostat.heating

    @heating.setter
    def heating(self, heat):
        self.heater.on() if heat else self.heater.off()

    def should_heat(self):
        return self.thermostat.check(self.current_temperature)

    def scheduled_temperature(self):
        return self.scheduled_temperature_for(now())

    def scheduled_temperature_for(self, a_datetime):
        return self.schedule.get_temperature_for(a_datetime)

    @property
    def schedule_days(self):
        return self.schedule.schedule

    def schedule_day_events(self, day):
        return self.schedule.schedule[day].items()

    def set_target_from_schedule(self):
        target_temperature = self.scheduled_temperature()
        if target_temperature != self.target_temperature:
            print("setting temperature to {}".format(target_temperature))
            self.target_temperature = target_temperature








