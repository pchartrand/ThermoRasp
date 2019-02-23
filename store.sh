#!/bin/bash
# usage: nohup $0 >/dev/null &
SLEEP=1799.77
while /bin/true; do
    curl -X POST -H 'Content-Type: application/json' -i 'http://localhost:5000/store' >/dev/null 2>/dev/null
    ./status.sh  |egrep -e 'Date|target' >>store.log 2>/dev/null
    sleep $SLEEP
done

