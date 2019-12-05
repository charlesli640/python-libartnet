# This file is a part of python-libartnet
#
# Copyright (C) 2013 Fredrik Lindberg <fli@shapeshifter.se>
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
from .node import *
from .libartnet import libartnet

class Artnet(object):

    (SRV, NODE, MSRV, ROUTE, BACKUP, RAW) = (0, 1, 2, 3, 4, 5)

    _num_ports = 0

    def __init__(self, type_=SRV, ip=None, verbose=0):
        if not libartnet:
            raise OSError("Unable to load libartnet")

        self._ip = ip
        self._verbose = int(verbose)
        if self._verbose:
            print("libartnet.artnet_new ip = {} type(ip)={}".format(ip, type(ip)))
        self._node = libartnet.artnet_new(bytes(bytearray(ip, 'utf-8')), self._verbose)
        if self._node == None:
            print("Create Node failed! return NULL")
        if self._verbose:
            print("Node IP={} self._node value={} type={}".format(ip, self._node, type_))
        self.type = type_
        self.subnet = 0
        self._CHANDLER = \
            CFUNCTYPE(c_int, c_void_p, c_void_p, c_void_p)
        self._handlers = {}
        self._ports = []

    def __del__(self):
        if self._node != None:
            libartnet.artnet_destroy(self._node)

    @property
    def handle(self):
        return self._node

    def start(self):
        ret = libartnet.artnet_start(self._node)

    def stop(self):
        ret = libartnet.artnet_stop(self._node)

    def read(self, timeout=0):
        ret = libartnet.artnet_read(self._node, timeout)

    def fileno(self):
        if self._node == None:
            print("NULL node")
            return -1
        ret = libartnet.artnet_get_sd(self._node)
        if self._verbose:
            print("fileno={}".format(ret))
        return ret

    TTM_DEFAULT = 0xFF
    TTM_PRIVATE = 0xFE
    TTM_AUTO = 0xFD

    def send_poll(self, ip=None, ttm=TTM_DEFAULT):
        return libartnet.artnet_send_poll(self._node, ip, ttm)

    @property
    def ip(self):
        return self._ip

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value
        if self._verbose:
            print("set nodetype: node = {} type={}".format(self._node, value))
        libartnet.artnet_set_node_type(self._node, value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        libartnet.artnet_set_short_name(self._node, value)

    @property
    def long_name(self):
        return self._name

    @long_name.setter
    def long_name(self, value):
        self._name = value
        libartnet.artnet_set_long_name(self._node, value)

    @property
    def broadcast_limit(self):
        return self._bcast_limit
    @broadcast_limit.setter
    def broadcast_limit(self, value):
        self._bcast_limit = value
        libartnet.artnet_set_bcast_limit(self._node, value)

    @property
    def subnet(self):
        return self._subnet
    @broadcast_limit.setter
    def subnet(self, value):
        self._subnet = value
        libartnet.artnet_set_subnet_addr(self._node, value)

    HANDLER_RECV = 0
    HANDLER_SEND = 1
    HANDLER_POLL = 2
    HANDLER_REPLY = 3
    HANDLER_DMX = 4
    HANDLER_ADDRESS = 5
    HANDLER_INPUT = 6
    HANDLER_TOD_REQUEST = 7
    HANDLER_TOD_DATA = 8
    HANDLER_TOD_CONTROL = 9
    HANDLER_RDM = 10
    HANDLER_IPPROG = 11
    HANDLER_FIRMWARE = 12
    HANDLER_FIRMWARE_REPLY = 13

    def _handler(self, node, pp, data):
        h = self._handlers[data]
        return h['cb'](self, h['data'])

    def set_handler(self, handler, cb, data=None):
        ccb = self._CHANDLER(self._handler)
        self._handlers[handler] = {
            'cb' : cb,
            'data' : data,
            'ccb' : ccb
        }
        libartnet.artnet_set_handler(self._node, handler, ccb, handler)

    def nodes(self):
        return Nodes(self._node)

    INPUT_PORT = 1
    OUTPUT_PORT = 2

    def add_port(self, prt):
        if self._num_ports >= 4:
            print("Failed to add port: port number exceeds 4!")
            return None
        id = self._num_ports
        self._num_ports = self._num_ports + 1

        libartnet.artnet_set_port_type(self._node, id, \
            prt.artnet_direction, prt.artnet_data_type)

        if prt.direction == prt.INPUT:
            direction = self.INPUT_PORT
        else:
            direction = self.OUTPUT_PORT
        if self._verbose:
            print("libartnet.artnet_set_port_addr id = {} addr = {}".format(id, prt.address))
        libartnet.artnet_set_port_addr(self._node, id, direction, \
            prt.address)

        self._ports.append(prt)
        prt.set_context(self)
        return id

    def ports(self):
        return filter(lambda x: x != None, self._ports)

class Controller(Artnet):

    def __init__(self, name = b"py-artnet", long_name = b"", ip=None, verbose=0):
        super(Controller, self).__init__(Artnet.SRV, ip, verbose)
        self.name = name
        self.long_name = long_name
        self.set_handler(self.HANDLER_POLL, self._handler_poll)
        self.set_handler(self.HANDLER_REPLY, self._handler_reply)
        self.start()

    def _handler_reply(self, artnet, data):
        return 0

    def _handler_poll(self, artnet, data):
        libartnet.artnet_send_poll_reply(self._node)
        return 0

    def discover(self):
        self.send_poll()

    def run(self):
        self.read()
