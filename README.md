# ThermoRasp
Thermostat made with a ARPI600 board on a raspberrypi 2.

## Requirements:

A 310 NTC thermistor and a 5k6 resistor for temperature measurement.

A SSRNC-430B solid-state relay with a 68 Ω series resistor for heater control. 

### Note:

You will need to add a connection between TLC1453 chip select (CS) pin and GPIO 
pin 19 to allow accurate temperature measurements. CS is not connected to the ARPI600 
board, so the measured values are erratic.

## Principle of operation:

The flask application integrates the different components 
(adc, temperature calculation, relay control, thermostat logic).

It makes system status and control possible thru a REST API.

## Testing:

`./test.py`

## Usage:

Start flask server

`./startup.sh`

Start polling process (checks temperature once a minute)

`nohup poll.sh &`

To check current status (temperature, target, heating):

`./status.sh`

To set thermostat to another temperature, say 21.5:

`./set.sh 21.5`

To force evaluation of current temperature:

`./check.sh`


 
