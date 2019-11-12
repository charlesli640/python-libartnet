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

def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

parser = argparse.ArgumentParser(description="libartnet python wrapper example: setdmx")
parser.add_argument("-p", "--port", type=int, dest="port", default=0,
                  help="Set port address")
parser.add_argument("-a", "--address", type=str, dest="ip", default="127.0.0.1",
                  help="IP address the artnet interface")
parser.add_argument(metavar='N', type=int, nargs='+', dest="channelvalues",
                    help='channel-value pairs')
args = parser.parse_args()

if len(args.channelvalues) % 2:
    parser.error("Channel and values should be specified in pairs")

print("DMX port = {}".format(args.port))
ac = artnet.Controller(b"pyartnet-setdmx", ip=args.ip, verbose=1)
# input data (DMX -> ArtNet) or output (ArtNet -> DMX) data
dp = artnet.port.DMX(int(args.port), artnet.port.DMX.INPUT)
ac.add_port(dp)

print("setdmx: Using port {}".format(dp))

for channel, value in pairwise(args.channelvalues):
    print("channel={} value={}".format(channel, value))
    dp.set(channel, value)
    print("Channel {}, set to {}".format(channel, value))
dp.send()
