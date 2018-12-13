# ThermoRasp
Thermostat made with an ARPI600 board on a raspberrypi 2

## to use:

Start flask server

`nohup python app.py &`

Start polling process

`nohup poll.sh &`

To check current status (temperature, target, heating):

`./status.sh`

To set thermostat to another temperature, say 21.5:

`./set.sh 21.5`

To force evaluation of current temperature:

`./check.sh`


 
