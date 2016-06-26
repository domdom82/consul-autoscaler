#!/bin/bash
set -ex

# Get cluster name
CLUSTER=$1

# Get cluster type
TYPE=$2

echo "*** BOOTING VM OF TYPE '$TYPE' IN CLUSTER '$CLUSTER' ***"

# Timestamp resolution in seconds. This should not clash as we are only going to add/remove one VM at a time.
TIMESTAMP=$(date +%s)

# Set unique hostname using cluster prefix
HOSTNAME="$CLUSTER-$TIMESTAMP"
echo "VM NAME: $HOSTNAME"
hostname $HOSTNAME

# Get ansible
apt-get install -y software-properties-common
apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install -y ansible

# Hand over to ansible
cd ansible
ansible-playbook -i env/$TYPE boot.yml

