#!/bin/bash
# usage: nohup $0 >/dev/null &
SLEEP=59.77
while /bin/true; do
    ./check.sh |egrep -e 'Date|target' >>poll.log
    sleep $SLEEP
done
