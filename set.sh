#!/bin/bash
if [ $# -eq 0 ]
  then
    echo "Please provide a target temperature in celsius"
    exit 1
else
    curl -X PUT -H 'Content-Type: application/json' -i 'http://localhost:5000/target' --data "{\"target\": $1}" >/dev/null
    ./status.sh
fi