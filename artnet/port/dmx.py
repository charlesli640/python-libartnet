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
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

from ctypes import create_string_buffer
from .port import Port
from ..libartnet import libartnet

class DMX(Port):
    def __init__(self, address = 0, direction = Port.INPUT):
        super(DMX, self).__init__(address, direction)
        self._data_type = Port.DMX
        self.reset()

    def reset(self):
        self._channels = bytearray(512)  #create_string_buffer(512)

    def set(self, channel, value):
        if channel >= 1 and channel <= 512:
            print("set channel={} value={}".format(channel, value))
            self._channels[channel - 1] = int(value) % 256
            print("set channels={}".format(repr(self._channels)))


    @property
    def channels(self):
        return self._channels

    @property
    def data(self):
        return self._channels

    def send(self):
        data = self.data
        char_array = create_string_buffer(bytes(data), len(data))
        print("before send id={} addr={} len(data)={} data={} data[0]={} char_array[0]={}".format(self._id, self.address, len(data), repr(data), data[0], char_array[0]))
        libartnet.artnet_send_dmx(self._artnet.handle, self._id, len(data), char_array)
