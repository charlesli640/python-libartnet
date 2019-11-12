# This file is a part of python-libartnet
#
# Copyright (C) 2015 Fredrik Lindberg <fli@shapeshifter.se>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from ctypes import *
import sys
import traceback

libartnet = None
try:
    libname="libartnet.so"
    if sys.platform.startswith("win"):
        libname = "libartnet.dll"
        print("load Windows dll: {}".format(libname))
    libartnet = CDLL(libname)
    libartnet.artnet_new.restype = c_void_p
    libartnet.artnet_new.argtypes = [c_char_p, c_int]
    libartnet.artnet_set_node_type.argtypes = [c_void_p, c_int]
    libartnet.artnet_set_subnet_addr.argtypes = [c_void_p, c_uint8]
    libartnet.artnet_set_short_name.argtypes = [c_void_p, c_char_p]
    libartnet.artnet_set_long_name.argtypes = [c_void_p, c_char_p]
    libartnet.artnet_set_handler.argtypes = [c_void_p, c_int, c_void_p, c_void_p]
    libartnet.artnet_start.argtypes = [c_void_p]
    libartnet.artnet_destroy.argtypes = [c_void_p]
    libartnet.artnet_send_poll.argtypes = [c_void_p, c_char_p, c_int]
    libartnet.artnet_get_sd.argtypes = [c_void_p]
    libartnet.artnet_set_port_addr.argtypes = [c_void_p, c_int, c_int, c_byte]
    libartnet.artnet_set_bcast_limit.argtypes = [c_void_p, c_int]
    libartnet.artnet_set_port_type.argtypes = [c_void_p, c_int, c_int, c_int]
    libartnet.artnet_send_poll_reply.argtypes = [c_void_p]
    libartnet.artnet_read.argtypes = [c_void_p, c_int]
    libartnet.artnet_get_nl.argtypes = [c_void_p]
    libartnet.artnet_get_nl.restype = c_void_p
    libartnet.artnet_nl_get_length.argtypes = [c_void_p]
    libartnet.artnet_nl_first.argtypes = [c_void_p]
    libartnet.artnet_nl_first.restype = c_void_p
    libartnet.artnet_nl_next.argtypes = [c_void_p]
    libartnet.artnet_nl_next.restype = c_void_p
    libartnet.artnet_send_dmx.argtypes = [c_void_p, c_int, c_int16, c_char_p]

except:
    traceback.print_exc()
    libartnet = None
