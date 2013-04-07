#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# Quad/Pi Engine Control
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

class VirtualEngineControl(object):
    """Engine control class working with virtual engines for testing purposes"""
    def __init__(self):
        self.status = False # on/off
        self.m1 = 0 # percent float
        self.m2 = 0
        self.m3 = 0
        self.m4 = 0
    def startup(self):
        """Start engines"""
        self.status = True
        self.m1, self.m2, self.m3, self.m4 = (0, 0, 0, 0)
    def shutdown(self):
        """Shutdown engines"""
        self.status = False
        self.m1, self.m2, self.m3, self.m4 = (0, 0, 0, 0)
    def get_power(self):
        """Get current engine power setting
        Returns engine power settings as tuple of four percentual values
        """
        return (self.m1, self.m2, self.m3, self.m4)
    def set_power(self, m):
        """Set engine power.
        Params:
            m .. power for each engine as tuple of four percentual values
        """
        self.m1, self.m2, self.m3, self.m4 = m
	def get_status(self):
		return self.status
