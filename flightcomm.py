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

class FlightComm(object):
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERR = 4
    prio = {1: 'DEBUG', 2: 'INFO', 3: 'WARN', 4: 'ERR'}

    def log(self, prio, msg):
        print self.prio[prio], msg

    def contact(self):
        pass

    def get_status(self):
        return True

    def get_controls(self):
        """Get positions of pilot controls
        Returns tuple of throttle, roll, pitch and yaw"""
        return (0,0,0,0)
