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
    def _update(self):
        pass
    def startup(self):
        """Start engines"""
        self.status = True
        self.m1, self.m2, self.m3, self.m4 = (0, 0, 0, 0)
        self._update()
    def shutdown(self):
        """Shutdown engines"""
        self.status = False
        self.m1, self.m2, self.m3, self.m4 = (0, 0, 0, 0)
        self._update()
    def get_power(self):
        """Get current engine power setting
        Returns engine power settings as tuple of four values
        """
        return (self.m1, self.m2, self.m3, self.m4)
    def set_power(self, m):
        """Set engine power.
        Params:
            m .. power for each engine as tuple of four values
        """
        self.m1, self.m2, self.m3, self.m4 = m
        self._update()
	def get_status(self):
		return self.status

class PWMEngineControl(VirtualEngineControl):
    value_off = 0.05
    value_min = 0.062
    value_max = 0.2
    def _calc_value(self, m):
        if self.status:
            value_range = self.value_max - self.value_min
            return self.value_min + (value_range / 1000.0 * m)
        else:
            return self.value_off

    def _update(self):
        with open('/var/run/pwm', 'w') as f:
            v1 = self._calc_value(self.m1)
            v2 = self._calc_value(self.m2)
            v3 = self._calc_value(self.m3)
            v4 = self._calc_value(self.m4)
            f.write('0=%f\n' % v1)
            f.write('1=%f\n' % v2)
            f.write('2=%f\n' % v3)
            f.write('3=%f\n' % v4)
            print v1, v2, v3, v4

