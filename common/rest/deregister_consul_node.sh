#!/bin/bash
#
#
# Deregister a given node from the catalog. This is usually done after destroying the node's VM
# Datacenter hard-coded to dc1 for now

if [ $# -ne 2 ]; then 
  echo "Usage: HOST NODE"
  exit -1
fi

HOST=$1
NODE=$2

curl -s -X PUT -H 'Content-Type: application/json' \
   -d '{
        "Datacenter": "dc1",
        "Node": "$NODE"
       }' "http://$HOST:8500/v1/catalog/deregister"
