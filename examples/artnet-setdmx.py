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

import time
import artnet
import argparse


def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)


parser = argparse.ArgumentParser(
    description="libartnet python wrapper example: setdmx")
parser.add_argument("-p", "--port", type=int, dest="port", default=0,
                    help="Set port address")
parser.add_argument("-a", "--address", type=str, dest="ip", default="127.0.0.1",
                    help="IP address the artnet interface")
parser.add_argument("-f", "--fade", type=int, dest="fade", default=0,
                    help="Fade time")
parser.add_argument("-v", "--verbose", type=int, dest="verbose", default=0,
                    help="Verbose mode")
parser.add_argument(metavar='N', type=int, nargs='+', dest="channelvalues",
                    help='channel-value pairs')
args = parser.parse_args()

if len(args.channelvalues) % 2:
    parser.error("Channel and values should be specified in pairs")

print("DMX port = {}".format(args.port))
ac = artnet.Controller(b"pyartnet-setdmx", ip=args.ip, verbose=args.verbose)
# input data (DMX -> ArtNet) or output (ArtNet -> DMX) data
dp = artnet.port.DMX(int(args.port), artnet.port.DMX.INPUT)
ac.add_port(dp)

print("setdmx: Using port {}".format(dp))

f = args.fade
timestart = time.time()
timeend = timestart
timecur = timestart
if f>0:
    timeend = timestart + f

alldata = bytearray(512)
delta = 0
while timecur <= timeend:
    for channel, value in pairwise(args.channelvalues):
        #print("channel={} value={}".format(channel, value))
        value += delta
        value %= 256
        print("current time={} value={:0d} 0x{:0x} percent={}".format(timecur, value, value, value*100//255))
        #dp.set(channel, value)
        if channel > 1 and channel <= 512:
            alldata[channel-1] = value
    dp.set_universe(alldata)
    dp.send()
    time.sleep(0.04)
    timecur = time.time()
    delta += 1
