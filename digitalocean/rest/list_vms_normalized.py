#!/usr/bin/env python
#
# List all VMs currently provisioned in a DigitalOcean account and returns them in a normalized fashion.

import sys
import os
import json
import subprocess

MYDIR=os.path.abspath(os.path.dirname(sys.argv[0]))

# Grab all VMs
def getAllVMs():
  cmd = [ '/bin/sh', MYDIR + '/list_vms.sh' ]
  output = subprocess.check_output(cmd)
  vms = json.loads(output)['droplets']
  return vms

def normalize(vm):
  # pull up public ip
  if vm['networks']:
    if vm['networks']['v4']:
      networks = vm['networks']['v4']
      for nw in networks:
        if nw['type'] == 'public':
          vm['ip'] = nw['ip_address']
          break

  return vm

# normalize VMs
def getNormalizedVMs(vms):
  for vm in vms:
    vm = normalize(vm)

  return vms

vms = getAllVMs()
normalized_vms = getNormalizedVMs(vms)
print json.dumps(normalized_vms)
