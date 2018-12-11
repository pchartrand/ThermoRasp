def convert_to_temperature(value):
    '''
    Assuming a third degree polynomial relationship between voltage
    and temperature with a voltage divider made of an ntc
    thermistor (pullup) and a 5k6 resistor (to ground).
    Voltage measured across the 5k6 resistor.
    '''
    REFERENCE_VOLTS = 5.04
    A = 3.296
    B = -22.378
    C = 70.951
    D = -49.382
    volts = (value / 1023.0) * REFERENCE_VOLTS;
    return A*volts**3 + B*volts**2 + C*volts + D
