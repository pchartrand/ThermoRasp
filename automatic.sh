#!/bin/bash
curl -X POST -H 'Content-Type: application/json' -i 'http://localhost:5000/automatic' --data "{}" >/dev/null 2>/dev/null
./status.sh