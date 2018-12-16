# ThermoRasp
Thermostat made with a ARPI600 board on a raspberrypi 2.
Uses a ntc and a 5k6 resistor for temperature measurement,
and a SSRNC-430B solid-state relay with a 68 Ω series resistor for heater control.     

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


 
