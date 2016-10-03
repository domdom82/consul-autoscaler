#!/bin/bash

SCRIPTDIR="$(cd $(dirname "$0")/ && pwd)"
HOSTNAME=$1
TOKEN="$(cat $SCRIPTDIR/../tokens/docker-autoscaler)"

if [ $# -ne 1 ]; then 
  echo "Usage: delete_vm.sh HOSTNAME"
  exit -1
fi

# get VM id
VM_ID="$($SCRIPTDIR/get_vm_by_name.py $HOSTNAME)"


curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "$BODY" "https://api.digitalocean.com/v2/droplets/$VM_ID"
