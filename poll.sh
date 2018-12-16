#!/bin/bash
# usage: nohup $0 &
SLEEP=59.8
while /bin/true; do
    ./check.sh |egrep -e 'Date|target'
    sleep $SLEEP
done
