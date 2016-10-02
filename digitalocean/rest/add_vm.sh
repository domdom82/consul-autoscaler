#!/bin/bash
set -e

SCRIPTDIR="$(cd $(dirname "$0")/ && pwd)"
CLUSTER=$1
TOKEN="$(cat $SCRIPTDIR/../tokens/docker-autoscaler)"
SSH_KEYS="['autoscaler-key']"
CLOUD_INIT="$(cat $SCRIPTDIR/../cloud-init/cloud-config.yml)"

if [ $# -ne 1 ]; then
  echo "Usage: add_vm.sh CLUSTER"
  exit -1
fi

# Timestamp resolution in seconds. This should not clash as we are only going to add/remove one VM at a time.
TIMESTAMP=$(date +%s)

# Set unique hostname using cluster prefix
HOSTNAME="$CLUSTER-$TIMESTAMP"
echo "VM NAME: $HOSTNAME"

BODY='{
    "name":"$HOSTNAME",
    "region":"nyc3",
    "size":"512mb",
    "image":"ubuntu-14-04-x64",
    "ssh_keys":$SSH_KEYS,
    "backups":false, 
    "ipv6":true,
    "user_data":"$CLOUD_INIT",
    "private_networking":null,
    "volumes": null}'


curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d "$BODY" "https://api.digitalocean.com/v2/droplets"
