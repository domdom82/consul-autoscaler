#!/bin/bash
set -e

SCRIPTDIR="$(cd $(dirname "$0")/ && pwd)"

TYPE=$1
SSH_KEY=$2
TOKEN=$3

SUPPORTED_TYPES=["digitalocean"]

if [ $# -ne 3 ]; then 
  echo "Usage: creds.sh type ssh_pub_key token"
  exit 1
fi

if [[ ${SUPPORTED_TYPES[*]} =~ $TYPE ]]; then 
    echo "Injecting credentials for type $TYPE"
else
    echo "Unsupported type $TYPE"
    exit 2
fi

echo "Storing token in $TYPE/tokens"
echo $TOKEN > $SCRIPTDIR/$TYPE/tokens/docker-autoscaler

echo "Generating cloud-config"
cd $SCRIPTDIR/$TYPE/cloud-init
cp cloud-config-template.yml cloud-config.yml
sed -i -e "s|{{autoscaler_pub_key}}|$SSH_KEY|g" cloud-config.yml
sed -i -e "s/{{token}}/$TOKEN/g" cloud-config.yml
