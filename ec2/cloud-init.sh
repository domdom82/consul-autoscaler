#!/bin/bash

set -ex

# This script be executed via cloud-init when the ec2 instance boots up the first time.

# Get cluster name from parm
CLUSTER = $1

if [[ $CLUSTER == "" ]]; then
  CLUSTER = "default"
fi

TYPE = "ec2"

# We only need git to pull in the bootstrapping code
  sudo apt-get update
  sudo apt-get install git -y
  git clone https://github.com/domdom82/consul-autoscaler.git
  cd consul-autoscaler
  source boot.sh $CLUSTER $TYPE