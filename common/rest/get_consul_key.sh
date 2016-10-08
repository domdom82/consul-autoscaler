#!/bin/bash
#
#
# Try to get the value of a key in the KV store of a consul cluster from a given host in the cluster

if [ $# -ne 2 ]; then 
  echo "Usage: HOST KEY"
  exit -1
fi

HOST=$1
KEY=$2

curl -s "http://$HOST:8500/v1/kv/$KEY"
