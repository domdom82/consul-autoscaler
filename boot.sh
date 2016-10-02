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


# Install docker
DOCKER_VERSION="1.12.1-0~trusty"

if [[ ! -f /usr/local/bin/docker ]]; then
    echo "Installing docker version $DOCKER_VERSION"
    sudo apt-get -y install apt-transport-https ca-certificates
    sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
    sudo sh -c "echo deb https://apt.dockerproject.org/repo ubuntu-trusty main  > /etc/apt/sources.list.d/docker.list"
    sudo apt-get -y update -qq
    sudo apt-get install -y --force-yes docker-engine=$DOCKER_VERSION
    sudo -E bash -c 'echo '\''DOCKER_OPTS="-H unix:///var/run/docker.sock --storage-driver=overlay"'\'' >> /etc/default/docker'
    sudo service docker restart
else
    echo "Docker already installed."
fi

docker version

echo "*** BOOT FINISHED ***"