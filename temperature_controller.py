import os

from scheduling.schedule import read_schedule
from scheduling.timeutils import now
from thermostat.adc import gpio_setup, gpio_cleanup, TLC
from thermostat.ntc import convert_to_temperature
from thermostat.relay import Relay
from thermostat.termostat import Thermostat


class TemperatureController(object):
    def __init__(self, target_temperature, hysteresis, adc_gpio_pin, relay_gpio_pin, schedule_file):
        gpio_setup()
        self.thermostat = Thermostat(target_temperature, hysteresis)
        self.adc = TLC(adc_gpio_pin)
        self.heater = Relay(relay_gpio_pin)
        self.schedule = read_schedule(os.path.join(os.path.dirname(__file__), schedule_file))

    def gpio_cleanup(self):
        gpio_cleanup()

    def get_target(self):
        return self.thermostat.target

    def get_formatted_target(self):
        return "{:.1f}".format(self.get_target())

    def is_heating(self):
        return self.thermostat.heating

    def should_heat(self):
        return self.thermostat.check(self.get_temperature())

    def set_target_temperature(self, target_temperature):
        self.thermostat.set_target(target_temperature)

    def get_scheduled_temperature(self):
        return self.get_scheduled_temperature_for(now())

    def get_scheduled_temperature_for(self, a_datetime):
        return self.schedule.get_temperature_for(a_datetime)

    def schedule_days(self):
        return self.schedule.schedule

    def schedule_day_events(self, day):
        return self.schedule.schedule[day].items()

    def set_target_from_schedule(self):
        target_temperature = self.get_scheduled_temperature()
        if target_temperature != self.get_target():
            print("setting temperature to {}".format(target_temperature))
            self.set_target_temperature(target_temperature)

    def get_temperature(self):
        return convert_to_temperature(self.adc.read())

    def get_formatted_temperature(self):
        return "{:.1f}".format(self.get_temperature())

    def start_heating(self):
        self.heater.on()

    def stop_heating(self):
        self.heater.off()










