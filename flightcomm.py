#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# Quad/Pi Flight Communicator
#
# Copyright 2013 Michal Belica <devel@beli.sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import sys
import socket
import struct
from cStringIO import StringIO

class CommError(Exception):
    pass
class ProtocolError(CommError):
    pass

class FlightComm(object):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERR = 4
    prio = {1: 'DEBUG', 2: 'INFO', 3: 'WARN', 4: 'ERR'}
    addr = ('127.0.0.1', 31512)

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.addr)
        self.sock.setblocking(0)
        self.controls = (0, 0, 0, 0)
        self.motors = (0, 0, 0, 0)
        self.status = 0
        self.remaddr = None

    def transmit(self):
        if self.remaddr:
            s = 'M'
            s += struct.pack('<hhhh',
                    self.motors[0],
                    self.motors[1],
                    self.motors[2],
                    self.motors[3],
                    )
            self.sock.sendto(s, self.remaddr)

    def _parse_packets(self, data):
        sio = StringIO(data)
        while True:
            c = sio.read(1)
            if len(c) == 0:
                break
            if c == 'C':
                # controls
                s = sio.read(8)
                if len(s) != 8:
                    print "Short packet received"
                else:
                    self.controls = struct.unpack('<hhhh', s)
                    print self.controls
            else:
                sys.stdout.write('unknown byte (%d)\n' % ord(c))

    def receive(self):
        done = False
        s = ''
        while not done:
            try:
                ss, self.remaddr = self.sock.recvfrom(4096)
                if len(ss) == 0:
                    done = True
                else:
                    s += ss
            except socket.error as e:
                if e[0] == 11: # Resource temporarily unavailable
                    done = True
                else:
                    raise
        if len(s) > 0:
            self._parse_packets(s)

    def log(self, prio, msg):
        print self.prio[prio], msg

    def get_status(self):
        return True

    def get_controls(self):
        """Get positions of pilot controls
        Returns tuple of throttle, roll, pitch and yaw"""
        self.receive()
        return self.controls

    def contact(self):
        pass

