# ThermoRasp
Thermostat made with a ARPI600 board on a raspberrypi 2.

## Requirements:

An [ARPI600](https://www.waveshare.com/wiki/ARPI600) or a [TLC1543 ADC](https://www.waveshare.com/wiki/TLC1543_ADC_Board) board.

A 310 NTC thermistor and a 5k6 resistor for temperature measurement.

A SSRNC-430B solid-state relay with a 68 Ω series resistor for heater control. 

### Note:

If you are using the ARPI600 board, you will need to add a connection between TLC1453 chip select (CS) pin and GPIO 
pin 19 to allow accurate temperature measurements. CS is not connected to the ARPI600 
board, so the measured values are erratic.

## Principle of operation:

The flask application integrates the different components 
(adc, temperature calculation, relay control, thermostat logic).

It makes system status and control possible thru a REST API.

Temperature control is done via a periodic temperature check REST call to the flask app.

Target temperature setting is done via another REST call.

## Dependencies

`sudo pip install flask`

`sudo pip install gpiozero`

## Integration testing:

To make sure the system components work properly, use the following python script :

`./test.py`

## Setup:

Start flask server

`./startup.sh`

Start polling process (checks temperature once a minute).

`nohup poll.sh &`

## Usage:

To check current status (temperature, target, heating):

`./status.sh`

To set thermostat to another target temperature, say 21.5:

`./set.sh 21.5`

To force evaluation of current temperature:

`./check.sh`


 
