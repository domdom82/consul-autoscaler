#!/usr/bin/env python
#
# Watch script that checks if VMs need to be added or removed from the cluster.

# TODO: import stuff from boot.py

import sys
import os
import json
import subprocess
import re
import base64
import time
import random
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)

MYDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
HOSTNAME=None
HOSTIP=None

if (len(sys.argv) != 2):
  print "Usage: nanny.py type"
  exit(-1);

TYPE=sys.argv[1]


def getHostName():
  cmd = [ 'hostname' ]
  output = subprocess.check_output(cmd)
  output = output.rstrip()
  return output

# Get host ip
def getHostIP(hostname):
  cmd = [ MYDIR + '/' + TYPE + '/rest/get_vm_ip_by_name.py', hostname ]
  output = subprocess.check_output(cmd)
  output = output.rstrip()
  return output

# Get cluster name from host name in the form <name>-<timestamp>
def getClusterName(hostname):
  clusterName = None;
  pattern = "(\w+)-(\w+)"
  result = re.match(pattern, hostname)
  if result != None:
    clusterName = result.group(1)
    timestamp = result.group(2)
  return clusterName

# Try to get the cluster leader from a cluster host
def getClusterLeader(host):
  cmd = [ '/bin/sh', MYDIR + '/common/rest/get_consul_leader.sh', host ]
  output = None
  try:
    output = subprocess.check_output(cmd)
  except subprocess.CalledProcessError, e:
    logging.warning("WARNING: Could not reach Consul on host %s" % host)

  return output

# Returns True if this host is the cluster leader.
def isClusterLeader(host):
  leader = getClusterLeader(host)
  if leader != None and leader.find(host) > -1:
    return True
  else:
    return False

# Returns the value (base64 decoded) for a given key in Consul KV
def getKey(host, key):
  cmd = [ '/bin/sh', MYDIR + '/common/rest/get_consul_key.sh', host, key ]
  value = None
  try:
    output = subprocess.check_output(cmd)
    key = json.loads(output)
    value_encoded = key[0]["Value"]
    value = base64.b64decode(value_encoded)
  except (subprocess.CalledProcessError, ValueError):
    logging.warning("WARNING: Could not read key %s from Consul on host %s" % (key, host))
  return value

# Get all nodes in this cluster
def getClusterNodes(host):
  cmd = [ '/bin/sh', MYDIR + '/common/rest/get_consul_nodes.sh', host ]
  nodes = None
  try:
    output = subprocess.check_output(cmd)
    nodes = json.loads(output)
  except subprocess.CalledProcessError, e:
    logging.warning("WARNING: Could not reach Consul on host %s" % host)
  return nodes

# Get all nodes that have a critical health state
def getCriticalNodes(host):
  cmd = [ '/bin/sh', MYDIR + '/common/rest/get_consul_health.sh', host, "critical" ]
  nodes = None
  try:
    output = subprocess.check_output(cmd)
    all_nodes = json.loads(output)
    nodes = [n for n in all_nodes if n["CheckID"] == "serfHealth"]
  except subprocess.CalledProcessError, e:
    logging.warning("WARNING: Could not reach Consul on host %s" % host)
  return nodes

# Get all nodes that have a non-critical health state
def getHealthyNodes(host):
  nodes = None
  all_nodes = getClusterNodes(host)
  critical_nodes = getCriticalNodes(host)
  def found(node, nodes):
    for n in nodes:
      if n["Node"] == node:
        return True
    return False

  nodes = [n for n in all_nodes if not found(n["Node"], critical_nodes)]
  return nodes

# Returns the size of the host's cluster
def getClusterSize(host):
  # get only non-critical nodes. critical nodes are deemed dead and will not be taken into account.
  nodes = getHealthyNodes(host)
  size = len(nodes) if nodes else None
  return size

# Adds a new VM into this cluster
def addVM(clusterName):
  logging.info("Provisioning a new host in cluster %s" % clusterName)
  cmd = [ MYDIR + '/' + TYPE + '/rest/add_vm.sh', clusterName ]
  output = None
  try:
    output = subprocess.check_output(cmd)
  except subprocess.CalledProcessError, e:
    logging.error("ERROR: Could not provision new host")
    logging.error("Exception is %s" % e)

# Deregister a given node from the catalog
def deregisterNode(host, node):
  logging.info("Deregistering node %s from catalog" % node)
  cmd = [ '/bin/sh', MYDIR + '/common/rest/deregister_consul_node.sh', host, node ]
  try:
    output = subprocess.check_output(cmd)
  except subprocess.CalledProcessError, e:
    logging.warning("WARNING: Could not reach Consul on host %s" % host)

# Remove a random VM from the cluster except self
def removeVM(host):
  all_nodes = getHealthyNodes(host)
  # remove self from list
  nodes = [n for n in all_nodes if n["Address"] != host]
  # pick a random host to kill
  node_to_kill = random.choice(nodes)
  hostname = node_to_kill["Node"]
  logging.info("Removing random host %s from cluster" % hostname)

  cmd = [ MYDIR + '/' + TYPE + '/rest/delete_vm.sh', hostname ]
  output = None
  try:
    output = subprocess.check_output(cmd)
    # deregister node from catalog to avoid stale node entries
    deregisterNode(host, hostname)
  except subprocess.CalledProcessError, e:
    logging.error("ERROR: Could not remove host %s" % hostname)
    logging.error("Exception is %s" % e)



############################################
# BEGIN MAIN PROGRAM
############################################

logging.info("HOSTS CHANGED START")

# Step 1. Get our own hostname and cluster name
logging.info("Cluster type is %s" % TYPE)
HOSTNAME=getHostName()
logging.info("Hostname is %s" % HOSTNAME)
HOSTIP=getHostIP(HOSTNAME)
logging.info("Host IP is %s" % HOSTIP)
CLUSTERNAME=getClusterName(HOSTNAME)

if CLUSTERNAME == None:
  logging.error("ERROR: Could not get cluster name from hostname %s" % HOSTNAME)
  exit(1)

logging.info("Cluster name is %s" % CLUSTERNAME)

# Step 2. Am I the leader?
if isClusterLeader(HOSTIP):
  logging.info("I am the cluster leader.")
  # Get cluster/desiredhosts
  desiredhosts = getKey(HOSTIP, "cluster/desiredhosts")
  if desiredhosts == None:
    logging.warning("Expected cluster/desiredhosts key in Consul KV.")
    exit(2)
  desiredhosts = int(desiredhosts)
  logging.info("cluster/desiredhosts is %s" % desiredhosts)
  # Get cluster size
  actualhosts = getClusterSize(HOSTIP)
  logging.info("actualhosts is %s" % actualhosts)
  # Need more VMs?
  if desiredhosts > actualhosts:
    logging.info("desiredhosts > actualhosts. Need to add a VM.")
    addVM(CLUSTERNAME)
  # Need fewer VMs?
  elif desiredhosts < actualhosts:
    logging.info("desiredhosts < actualhosts. Need to remove a VM.")
    removeVM(HOSTIP)
  # Nothing to do
  else:
    logging.info("desiredhosts == actualhosts. Nothing to do.")
else:
  logging.info("I am not the cluster leader. Nothing to do.")

logging.info("HOSTS CHANGED END")
