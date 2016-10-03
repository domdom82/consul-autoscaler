#!/bin/bash
set -e

# Get cluster type
TYPE=$1

# TBD: Get cluster name from hostname
CLUSTER=$(hostname)

echo "*** BOOTING VM OF TYPE '$TYPE' IN CLUSTER '$CLUSTER' ***"

# Install docker
DOCKER_VERSION="1.12.1-0~trusty"

if [[ ! -f /usr/local/bin/docker ]]; then
    echo "Installing docker version $DOCKER_VERSION"
    apt-get -y install apt-transport-https ca-certificates
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
    sh -c "echo deb https://apt.dockerproject.org/repo ubuntu-trusty main  > /etc/apt/sources.list.d/docker.list"
    apt-get -y update -qq
    apt-get install -y --force-yes docker-engine=$DOCKER_VERSION
    bash -c 'echo '\''DOCKER_OPTS="-H unix:///var/run/docker.sock --storage-driver=overlay"'\'' >> /etc/default/docker'
    service docker restart
else
    echo "Docker already installed."
fi

docker version

# Launch boot.py
boot.py $TYPE

echo "*** BOOT FINISHED ***"
