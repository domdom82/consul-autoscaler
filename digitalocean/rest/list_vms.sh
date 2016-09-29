#!/bin/bash
#
#
# List all VMs currently provisioned in a DigitalOcean account

if [ $# -ne 1 ]; then 
  echo "Usage: list_vms.sh TOKEN"
  exit -1
fi

TOKEN=$1

curl -s -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" "https://api.digitalocean.com/v2/droplets"