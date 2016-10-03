#!/usr/bin/env python
#
# Returns a vm id for a VM name

import sys
import os
import json
import subprocess

if (len(sys.argv) != 2):
  print "Usage: get_vm_by_name name"
  exit(-1);

MYDIR=os.path.abspath(os.path.dirname(sys.argv[0]))
HOSTNAME=sys.argv[1]

# Grab all VMs to get their ids
def getAllVMs():
  cmd = [ '/bin/sh', MYDIR + '/list_vms.sh' ]
  output = subprocess.check_output(cmd)
  vms = json.loads(output)['droplets']
  return vms

# get the VM id for name
def getVMId(vms, name):
  details = []
  for vm in vms:
    host = vm['name']
    id = vm['id']
    if host == name:
      return id;
  return -1

vms = getAllVMs()
vmId = getVMId(vms, HOSTNAME);
print vmId
