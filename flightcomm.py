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

import socket
import struct

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
        self.controls = (0, 0, 0, 0)

    def receive(self):
        try:
            s = self.sock.recv(4)
        except socket.error as e:
            if e[0] == 11:
                # no data
                pass
            else:
                raise
        else:
            self.controls = struct.unpack('<bbbb', s)

    def log(self, prio, msg):
        print self.prio[prio], msg

    def contact(self):
        self.sock.connect(self.addr)
        self.sock.sendall('Quad/Pi P1\n')
        s = self.sock.recv(3)
        if s != 'OK\n':
            raise ProtocolError('Handshake fail')
        self.sock.setblocking(0)

    def get_status(self):
        return True

    def get_controls(self):
        """Get positions of pilot controls
        Returns tuple of throttle, roll, pitch and yaw"""
        self.receive()
        return (0,0,0,0)

