"""JVPN netstats libraries

"""

__author__ = 'e@dscp.org (Ebben Aries)'

import socket
import struct

def GetNetstats(device):
  device = device + ':'
  for line in open('/proc/net/dev', 'r'):
    data = filter(None, line.split(' '))
    if data[0] == device:
      return (data[1], data[2], data[9], data[10])

def GetRoutes(device):
  routes = []
  for line in open('/proc/net/route', 'r'):
    if line.startswith(device):
      prefix = socket.inet_ntoa(struct.pack('<L', int(line.split()[1], 16)))
      metric = int(line.split()[6])
      netmask = socket.inet_ntoa(struct.pack('<L', int(line.split()[7], 16)))
      route_detail = '%s/%s:%d' % (prefix, netmask, metric)
      routes.append(route_detail)
  return routes

def GetIp(device):
  ip = ''
  for line in open('/proc/net/route', 'r'):
    if line.startswith(device):
      ip = socket.inet_ntoa(struct.pack('<L', int(line.split()[2], 16)))
      break
  return ip

def GetDefInterface(interface='eth0', gateway='0.0.0.0'):
  for line in open('/proc/net/route', 'r'):
    if line.split()[1] == '00000000' and line.split()[7] == '00000000':
      interface = line.split()[0]
      gateway = socket.inet_ntoa(struct.pack('<L', int(line.split()[2], 16)))
  return gateway, interface


