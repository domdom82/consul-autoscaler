#!/bin/bash
set -e

# Get cluster type
TYPE=$1

# Get cluster name
CLUSTER=$2

echo "*** BOOTING VM OF TYPE '$TYPE' IN CLUSTER '$CLUSTER' ***"

# Timestamp resolution in seconds. This should not clash as we are only going to add/remove one VM at a time.
TIMESTAMP=$(date +%s)

# Set unique hostname using cluster prefix
HOSTNAME="$CLUSTER-$TIMESTAMP"
echo "VM NAME: $HOSTNAME"
hostname $HOSTNAME


# Get docker-machine
DOCKER_MACHINE_VERSION="v0.8.2"

if [[ ! -f /usr/local/bin/docker-machine ]]; then
    echo "Installing docker machine version $DOCKER_MACHINE_VERSION"
    curl -L "https://github.com/docker/machine/releases/download/$DOCKER_MACHINE_VERSION/docker-machine-$(uname -s)-$(uname -m)" > /usr/local/bin/docker-machine
    chmod +x /usr/local/bin/docker-machine
fi

docker-machine --version

echo "*** BOOT FINISHED ***"