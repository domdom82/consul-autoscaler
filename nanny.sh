#!/bin/bash
set -e

SCRIPTDIR="$(cd $(dirname "$0")/ && pwd)"

echo "AUTOSCALER_TYPE == $AUTOSCALER_TYPE"

cd $SCRIPTDIR
./nanny.py $AUTOSCALER_TYPE
