#!/bin/bash
#
#
# List all VMs currently provisioned in a DigitalOcean account

SCRIPTDIR="$(cd $(dirname "$0")/ && pwd)"
TOKEN="$(cat $SCRIPTDIR/../tokens/docker-autoscaler)"

curl -s -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" "https://api.digitalocean.com/v2/droplets"