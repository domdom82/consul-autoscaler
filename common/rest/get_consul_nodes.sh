#!/bin/bash
#
#
# Try to get the nodes of a consul cluster from a given host in the cluster

if [ $# -ne 1 ]; then 
  echo "Usage: HOST"
  exit -1
fi

HOST=$1

curl -s "http://$HOST:8500/v1/catalog/nodes"
