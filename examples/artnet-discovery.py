#!/usr/bin/env python
# Copyright (C) 2013 Fredrik Lindberg <fli@shapeshifter.se>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

from __future__ import print_function

import artnet
from select import select
import argparse
from time import time

print("Start...")
parser = argparse.ArgumentParser(description="libartnet python wrapper example: discovery")
parser.add_argument('-t', dest='timeout', type=int, default=3, help="Discovery timeout")
parser.add_argument("-a", dest="ip", type=str, default="127.0.0.1", help="IP address the artnet interface")
parser.add_argument("-v", dest="verbose", type=int, default=0, help="verbose")
args = parser.parse_args()

print("timeout={}".format(args.timeout))
print("ip={}".format(args.ip))

ac = artnet.Controller(b"pyartnet-discover", ip=args.ip, verbose=args.verbose)

ac.discover()

start = time()
while (time() - start) < int(args.timeout):
    if args.verbose:
        print("timeout={} ac={}".format(args.timeout, ac))
    readable, writeable, exception = select([ac], [], [], 1)
    if len(readable) > 0:
        ac.run()

for node in ac.nodes():
    print("IP: {} Mac: {}".format(node.ip, node.mac))
    print("Name: {}\nVersion: {}".format(node.name.decode('utf-8'), node.version))
    print("Subnet: {}".format(node.subnet))
    print("Ports: {}".format(node.ports))
