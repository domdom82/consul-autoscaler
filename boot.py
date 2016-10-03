#!/usr/bin/env python
#
# Seed script that joins a new VM into an existing cluster or creates a new one.
# The decision to create a new cluster is based on the existence of VMs with the same prefix.
#

# TODO: need logging

import sys
import os
import json
import subprocess
import re

MYDIR = os.path.abspath(os.path.dirname(sys.argv[0]))
HOSTNAME=None
HOSTIP=None
PEER_LIMIT=5

if (len(sys.argv) != 2):
  print "Usage: boot.py type"
  exit(-1);

TYPE=sys.argv[1]

def getBaseCmd():
  cmd=[ 'docker', 'run', '-d', '--net', 'host','--name', 'consul', '-h', HOSTNAME, '-e', 'CONSUL_LOCAL_CONFIG={"leave_on_terminate": true}', 'consul', 'agent', '-advertise', HOSTIP, '-client=0.0.0.0' ]
  return cmd

def startRegistrator():
  print "Starting registrator..."
  cmd=[ 'docker', 'run','-d', '--name', 'registrator', '--net', 'host', '-v', '/var/run/docker.sock:/tmp/docker.sock', 'gliderlabs/registrator', 'consul://localhost:8500' ]
  output = subprocess.check_output(cmd)
  return output

def cleanContainers():
  print "Cleaning all containers..."
  cmd=[ '/bin/sh', 'docker', 'rm', '-f', '$(docker ps -aq)']
  output = subprocess.check_output(cmd)
  return output

def getHostName():
  cmd = [ 'hostname' ]
  output = subprocess.check_output(cmd)
  output = output.rstrip()
  return output

# Get host backend ip from SoftLayer
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
    clustername = result.group(1)
    timestamp = result.group(2)
  return clusterName

# Get all machines in this cluster
def getCluster(clusterName):
  cmd = [ '/bin/sh', MYDIR + '/' + TYPE + '/rest/list_vms_by_prefix.py', clusterName ]
  output = subprocess.check_output(cmd)
  instances = json.loads(output)
  return instances

# Try to get the cluster leader from a cluster host
def getClusterLeader(host):
  cmd = [ '/bin/sh', MYDIR + '/common/rest/get_consul_leader.sh', host ]
  output = None
  try:
    output = subprocess.check_output(cmd)
  except subprocess.CalledProcessError, e:
    print "WARNING: Could not reach Consul on host %s" % host

  return output

# Try to get the cluster peers (i.e. replication hosts) from a cluster host
def getClusterPeers(host):
  cmd = [ '/bin/sh', MYDIR + '/common/rest/get_consul_peers.sh', host ]
  peers = []
  try:
    output = subprocess.check_output(cmd)
    peers = json.loads(output)
  except subprocess.CalledProcessError, e:
    print "WARNING: Could not reach Consul on host %s" % host
    print "Exception: %s", e

  return peers

# Start a new cluster. Start a server in bootstrap mode
def startCluster():
  print "Starting new cluster"
  cmd = getBaseCmd()
  cmd.extend(['-server', '-bootstrap'])
  output = subprocess.check_output(cmd)

# Join an existing cluster as a server
def joinClusterAsServer(host):
  print "Joining cluster %s at node %s as a server" % (CLUSTERNAME, host)
  cmd = getBaseCmd()
  cmd.extend(['-server', '-join', host ])
  output = subprocess.check_output(cmd)

# Join an existing cluster as a plain agent
def joinClusterAsAgent(host):
  print "Joining cluster %s at node %s as an agent" % (CLUSTERNAME, host)
  cmd = getBaseCmd()
  cmd.extend(['-join', host ])
  output = subprocess.check_output(cmd)

# Join an existing cluster. If a cluster has less than 5 replication hosts, start a server, else start just an agent
def joinCluster(clusterHosts):
  print "Joining existing cluster %s" % CLUSTERNAME
  for host in clusterHosts:
    hostip = host['ip']
    leader = getClusterLeader(hostip)
    if leader != None:
      print "Cluster leader is %s" % leader
      peers = getClusterPeers(hostip)
      print "Cluster servers are %s" % peers
      print "Number of servers is %s" % len(peers)
      if len(peers) < PEER_LIMIT:
        print "There are fewer than %s servers in this cluster" % PEER_LIMIT
        joinClusterAsServer(hostip)
      else:
        print "There are at least %s servers in this cluster" % PEER_LIMIT
        joinClusterAsAgent(hostip)
      return

  # None of the hosts reachable? Assume cluster is dead. Start new one.
  print "No cluster hosts could be reached. Assume cluster is dead. Starting new one."
  startCluster()

############################################
# BEGIN MAIN PROGRAM
############################################

print "CLUSTER BOOT START\n"

# Step 1. Get our own hostname and cluster name
HOSTNAME=getHostName()
print "Hostname is %s" % HOSTNAME
HOSTIP=getHostIP(HOSTNAME)
print "Host IP is %s" % HOSTIP
CLUSTERNAME=getClusterName(HOSTNAME)

if CLUSTERNAME == None:
  print "ERROR: Could not get cluster name from hostname %s" % HOSTNAME
  exit(1)

print "Cluster name is %s" % CLUSTERNAME

# Step 2. Try to find an existing cluster to join
CLUSTER=getCluster(CLUSTERNAME)

# Step 3. Remove old containers if they exist
cleanContainers()

# Step 4. Start a new cluster or join an existing one
if len(CLUSTER) == 0:
  startCluster()
else:
  joinCluster(CLUSTER)

# Step 5. Start registrator
startRegistrator()

print "\nCLUSTER BOOT END"
