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

#from IMU_sensors.itg3200 import SensorITG3200
from virtualsensors import VirtualSensor as SensorITG3200
from enginecontrol import VirtualEngineControl
from flightcomm import FlightComm

GYRO_GAIN = (0.01, 0.01, 0.01)
GYRO_MIN = 5 # minimum threshold
CONTROL_GAIN = (1, 1, 1)

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
        self.comm.log(self.comm.INFO, "starting engine")
        self.engine.startup()
        while not self.engine.get_status():
            time.sleep(0.2)
        self.comm.log(self.comm.INFO, "engine READY")
        while True:
            self.control_loop()

    def control_loop(self):
        gx, gy, gz = self.gyro.read_data()
        m1, m2, m3, m4 = self.engine.get_power()
        thr, roll, pitch, yaw = self.comm.get_controls()
        
        om1, om2, om3, om4 = (thr, thr, thr, thr)

        # X-axis (roll) stabilization
        if abs(gx) > GYRO_MIN:
            om1 += GYRO_GAIN[0] * gx
            om2 += GYRO_GAIN[0] * gx
            om3 += GYRO_GAIN[0] * gx
            om4 += GYRO_GAIN[0] * gx
        # Y-axis (pitch) stabilization
        if abs(gy) > GYRO_MIN:
            om1 += GYRO_GAIN[1] * gy
            om2 += GYRO_GAIN[1] * gy
            om3 += GYRO_GAIN[1] * gy
            om4 += GYRO_GAIN[1] * gy
        # Z-axis (yaw) stabilixation
        if abs(gz) > GYRO_MIN:
            om1 += GYRO_GAIN[2] * gz
            om2 += GYRO_GAIN[2] * gz
            om3 += GYRO_GAIN[2] * gz
            om4 += GYRO_GAIN[2] * gz

        # roll control
        om1 += CONTROL_GAIN[0] * roll
        om2 += CONTROL_GAIN[0] * roll
        om3 += CONTROL_GAIN[0] * roll
        om4 += CONTROL_GAIN[0] * roll
        # pitch control
        om1 += CONTROL_GAIN[1] * pitch
        om2 += CONTROL_GAIN[1] * pitch
        om3 += CONTROL_GAIN[1] * pitch
        om4 += CONTROL_GAIN[1] * pitch
        # yaw control
        om1 += CONTROL_GAIN[2] * yaw
        om2 += CONTROL_GAIN[2] * yaw
        om3 += CONTROL_GAIN[2] * yaw
        om4 += CONTROL_GAIN[2] * yaw
        
        self.engine.set_power((om1, om2, om3, om4))
        print int(om1), int(om2), int(om3), int(om4)
        time.sleep(0.2)


if __name__ == '__main__':
    flight = Flight(
        VirtualEngineControl(),
        SensorITG3200(1, 0x68),
        FlightComm()
        )
    flight.take_control()
