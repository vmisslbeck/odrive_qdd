#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function
from odrive.enums import *
import time
import odrv_movements
import odrv_con_and_calib

cc = odrv_con_and_calib
mvmts = odrv_movements

my_drive = cc.find_one_odrive()
cc.check_voltage(my_drive)

time.sleep(1)
my_drive.clear_errors() # this clear_errors is critical, otherwise we always get ERRORS
my_drive.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
print("setpoint: " + str(my_drive.axis0.controller.pos_setpoint))

time.sleep(1)

move = mvmts.position_movements(my_drive)
vel_move = mvmts.velocity_movements(my_drive)

# A sine wave to test
t0 = time.monotonic()
try:
    vel_move.move_back_and_forth(10, 10)
    while True:

        move.sine_wave(t0)

except KeyboardInterrupt:
    my_drive.axis0.requested_state = AxisState.IDLE
    print("Motor stopped.")
    pass
