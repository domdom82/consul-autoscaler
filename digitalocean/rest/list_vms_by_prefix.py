#!/usr/bin/env python
#
# Returns a vm ip for a VM name

import sys
import os
import json
import subprocess
import re

if (len(sys.argv) != 2):
  print "Usage: list_vms_by_prefix prefix"
  exit(-1);

MYDIR=os.path.abspath(os.path.dirname(sys.argv[0]))
HOSTNAME=sys.argv[1]

# Grab all VMs
def getAllVMs():
  cmd = [ MYDIR + '/list_vms_normalized.py' ]
  output = subprocess.check_output(cmd)
  vms = json.loads(output)
  return vms

# get the VMs filtered by prefix
def getPrefixVMs(vms, prefix):
  def prefixFilter(vm):
    pattern = "(\w+)-(\w+)"
    result = re.match(pattern, vm['name'])
    if result != None:
      vmprefix = result.group(1)
      if vmprefix == prefix:
        return True
    return False

  return filter(prefixFilter, vms)

vms = getAllVMs()
prefix_vms = getPrefixVMs(vms, HOSTNAME)
print json.dumps(prefix_vms)
