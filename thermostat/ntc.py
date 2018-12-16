def convert_to_temperature(value):
    '''
    :value is an integer between 0 and 1023.

    Assuming a third degree polynomial relationship between voltage
    and temperature with a voltage divider made of an NTC 310
    thermistor (pullup) and a 5k6 resistor (to ground).
    Voltage is measured across the 5k6 resistor.
    More info here
    https://github.com/pchartrand/temperature-monitor/blob/master/Samples/ntc_measurements_and_polynomial_regression.png

    This is more empirical than the Steinhart–Hart coefficients approach,
    but yields good results in normal temperature ranges.

    https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation
    '''
    REFERENCE_VOLTS = 5.04
    A = 3.296
    B = -22.378
    C = 70.951
    D = -49.382
    volts = (value / 1023.0) * REFERENCE_VOLTS;
    return A*volts**3 + B*volts**2 + C*volts + D
