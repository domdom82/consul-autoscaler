#!/bin/bash

HOSTNAME=$1
TOKEN=$2

if [ $# -ne 2 ]; then 
  echo "Usage: delete_vm.sh HOSTNAME TOKEN"
  exit -1
fi
