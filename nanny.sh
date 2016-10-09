#!/bin/bash

SCRIPTDIR="$(cd $(dirname "$0")/ && pwd)"

echo "nanny.sh start at $(date)" >> /logs/nanny.log

cd $SCRIPTDIR
./nanny.py $AUTOSCALER_TYPE >> /logs/nanny.log 2>&1

echo "nanny.sh stop at $(date)" >> /logs/nanny.log
