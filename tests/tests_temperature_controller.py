from unittest import TestCase

from mock import MagicMock, patch
class TestsTemperatureController(TestCase):
    RELAY_GPIO_PIN = 17
    ADC_GPIO_PIN = 6

    @patch('gpiozero.LED')
    def test_i_can_mock_relay_to_bypass_gpio(self, MockLed):
        from thermostat.relay import Relay
        relay = Relay(self.RELAY_GPIO_PIN)
        relay.relay.on = MagicMock()
        relay.relay.off = MagicMock()
        relay.on()
        relay.off()

        relay.relay.on.assert_called_once()
        relay.relay.off.assert_called_once()

    @patch('RPi.GPIO')
    def test_i_can_mock_adc_to_bypass_gpio(self, MockGPIO):
        from thermostat.adc import TLC
        adc = TLC(self.ADC_GPIO_PIN)
        adc.read = MagicMock(return_value=512)

        value = adc.read()
        assert value == 512
        adc.read.assert_called_once()

    @patch('RPi.GPIO')
    @patch('thermostat.relay.Relay')
    @patch('thermostat.adc.TLC')
    def test_i_can_create_a_temp_controller_and_fake_io(self, MockGPIO, MockTLD, MockRelay):
        INITIAL_TARGET_TEMPERATURE = 20
        HYSTERESIS = 0.5
        INITIAL_SCHEDULE_FILE = 'schedule.yml'
        from thermostat.temperature_controller import TemperatureController
        TemperatureController.setup = MagicMock()
        tc = TemperatureController(
            INITIAL_TARGET_TEMPERATURE,
            HYSTERESIS,
            self.ADC_GPIO_PIN,
            self.RELAY_GPIO_PIN,
            INITIAL_SCHEDULE_FILE
        )
        tc.cleanup = MagicMock()
        tc.adc = MagicMock()
        tc.heater = MagicMock()
        tc.heater.on = MagicMock()
        tc.heater.off = MagicMock()

        assert tc.target_temperature == INITIAL_TARGET_TEMPERATURE

        tc.adc.read = MagicMock(return_value=322)

        assert round(tc.current_temperature) == 20, tc.current_temperature

        tc.target_temperature = 22

        assert tc.should_heat()
        assert tc.heating

        tc.target_temperature = 18

        assert not tc.should_heat()
        assert not tc.heating