#!/usr/bin/env python
#
# Returns an ssh key id for a ssh key name

import sys
import os
import json
import subprocess

if (len(sys.argv) != 2):
  print "Usage: get_key_by_name name"
  exit(1);

MYDIR=os.path.abspath(os.path.dirname(sys.argv[0]))
KEY=sys.argv[1]

# Grab all keys to get their ids
def getAllKeys():
  cmd = [ '/bin/sh', MYDIR + '/list_keys.sh' ]
  output = subprocess.check_output(cmd)
  vms = json.loads(output)['ssh_keys']
  return vms

# get the key id for name
def getKeyId(keys, name):
  details = []
  for key in keys:
    kn = key['name']
    id = key['id']
    if kn == name:
      return id;
  return -1

keys = getAllKeys()
keyId = getKeyId(keys, KEY);
print keyId
