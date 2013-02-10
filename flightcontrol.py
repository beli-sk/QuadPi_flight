#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# Quad/Pi Flight Controller
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

import time

from IMU_sensors.itg3200 import SensorITG3200 as Sensor
#from virtualsensors import VirtualSensor as Sensor
from enginecontrol import PWMEngineControl as EngineControl
#from enginecontrol import VirtualEngineControl as EngineControl
from flightcomm import FlightComm

GYRO_GAIN = (0.05, -0.05, 0.05)
GYRO_MIN = 5 # minimum threshold
CONTROL_GAIN = (1, 1, 1)

def crop_range(v, min, max):
    if v < min:
        return min
    elif v > max:
        return max
    else:
        return v

class Flight(object):
    def __init__(self, engine, gyro, comm):
        self.engine = engine
        self.gyro = gyro
        self.comm = comm

    def take_control(self):
        """Entry point"""
        self.comm.log(self.comm.INFO, "init comm")
        self.comm.contact()
        while not self.comm.get_status():
            time.sleep(0.2)
        self.comm.log(self.comm.INFO, "comm READY")
        self.comm.log(self.comm.INFO, "init gyro")
        self.gyro.default_init()
        while True:
            self._control_loop()

    def _calculate_power(self, gyro, controls):
        gx, gy, gz = gyro
        print (gx, gy, gz)
        thr, pitch, roll, yaw = controls
        om1, om2, om3, om4 = (thr, thr, thr, thr)

        # X-axis (roll) stabilization
        if abs(gx) > GYRO_MIN:
            om1 += GYRO_GAIN[0] * gx
            om2 -= GYRO_GAIN[0] * gx
            om3 += GYRO_GAIN[0] * gx
            om4 -= GYRO_GAIN[0] * gx
        # Y-axis (pitch) stabilization
        if abs(gy) > GYRO_MIN:
            om1 += GYRO_GAIN[1] * gy
            om2 += GYRO_GAIN[1] * gy
            om3 -= GYRO_GAIN[1] * gy
            om4 -= GYRO_GAIN[1] * gy
        # Z-axis (yaw) stabilixation
        if abs(gz) > GYRO_MIN:
            om1 += GYRO_GAIN[2] * gz
            om2 -= GYRO_GAIN[2] * gz
            om3 -= GYRO_GAIN[2] * gz
            om4 += GYRO_GAIN[2] * gz

        # roll control
        om1 += CONTROL_GAIN[0] * roll
        om2 -= CONTROL_GAIN[0] * roll
        om3 += CONTROL_GAIN[0] * roll
        om4 -= CONTROL_GAIN[0] * roll
        # pitch control
        om1 += CONTROL_GAIN[1] * pitch
        om2 += CONTROL_GAIN[1] * pitch
        om3 -= CONTROL_GAIN[1] * pitch
        om4 -= CONTROL_GAIN[1] * pitch
        # yaw control
        om1 += CONTROL_GAIN[2] * yaw
        om2 -= CONTROL_GAIN[2] * yaw
        om3 -= CONTROL_GAIN[2] * yaw
        om4 += CONTROL_GAIN[2] * yaw

        om1 = crop_range(om1, 0, 1000)
        om2 = crop_range(om2, 0, 1000)
        om3 = crop_range(om3, 0, 1000)
        om4 = crop_range(om4, 0, 1000)

        return (om1, om2, om3, om4)

    def _control_loop(self):
        gx, gy, gz = self.gyro.read_data()
        #m1, m2, m3, m4 = self.engine.get_power()
        thr, roll, pitch, yaw = self.comm.get_controls()
        if thr == 0:
            # engine off
            if self.engine.get_status():
                self.comm.log(self.comm.INFO, "engine shutdown")
                self.engine.shutdown()
            om1, om2, om3, om4 = (0,0,0,0)
        else:
            # engine on
            if not self.engine.get_status():
                self.comm.log(self.comm.INFO, "engine startup")
                self.engine.startup()
            om1, om2, om3, om4 = self._calculate_power((gx, gy, gz), (thr, pitch, roll, yaw))
            self.engine.set_power((om1, om2, om3, om4))
            #print int(om1), int(om2), int(om3), int(om4)
        self.comm.motors = (om1, om2, om3, om4)
        self.comm.transmit()
        time.sleep(0.04)


if __name__ == '__main__':
    flight = Flight(
        EngineControl(),
        Sensor(1, 0x68),
        FlightComm()
        )
    flight.take_control()
