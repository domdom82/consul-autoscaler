#!/bin/bash
set -e

SCRIPTDIR="$(cd $(dirname "$0")/ && pwd)"

echo "nanny.sh start at $(date)" >> /logs/nanny.log

cd $SCRIPTDIR
./nanny.py $AUTOSCALER_TYPE >> /logs/nanny.log

echo "nanny.sh stop at $(date)" >> /logs/nanny.log
echo "\n\n" >> /logs/nanny.log
