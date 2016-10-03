#!/usr/bin/env python
#
# Returns a vm ip for a VM name

import sys
import os
import json
import subprocess

if (len(sys.argv) != 2):
  print "Usage: get_vm_ip_by_name name"
  exit(-1);

MYDIR=os.path.abspath(os.path.dirname(sys.argv[0]))
HOSTNAME=sys.argv[1]

# Grab all VMs to get their ips
def getAllVMs():
  cmd = [ '/bin/sh', MYDIR + '/list_vms.sh' ]
  output = subprocess.check_output(cmd)
  vms = json.loads(output)['droplets']
  return vms

# get the VM ip for name
def getVMIP(vms, name):
  details = []
  for vm in vms:
    host = vm['name']
    networks = vm['networks']['v4']
    if host == name:
      for nw in networks:
        if nw['type'] == 'public':
          return nw['ip_address']
  return -1

vms = getAllVMs()
vmIP = getVMIP(vms, HOSTNAME);
print vmIP
