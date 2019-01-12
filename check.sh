#!/bin/bash
curl -X POST -H 'Content-Type: application/json' -i 'http://localhost:5000/heating' >/dev/null 2>/dev/null
./status.sh 2>/dev/null