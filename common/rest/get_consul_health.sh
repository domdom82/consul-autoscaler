#!/bin/bash
#
#
# Get all nodes and health checks in the specified state

if [ $# -ne 2 ]; then 
  echo "Usage: HOST STATE"
  exit -1
fi

HOST=$1
STATE=$2

curl -s "http://$HOST:8500/v1/health/state/$STATE"
