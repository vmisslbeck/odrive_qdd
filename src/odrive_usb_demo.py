#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

def calibrate_motor(motor):
    print("Calibrating motor...")
    motor.requested_state = AxisState.FULL_CALIBRATION_SEQUENCE
    while motor.current_state != AxisState.IDLE:
        time.sleep(0.1)
    print("Motor calibrated.")
    motor.requested_state = AxisState.CLOSED_LOOP_CONTROL


# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
print(odrive.connected_devices)
print(odrive.find_any())
my_drive = odrive.find_any()
print(odrive.find_any())
print("Odrive found!")
print(odrive.connected_devices)
my_drive.clear_errors()

# Calibrate motor and wait for it to finish



# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Or to change a value, just assign to the property
my_drive.axis0.controller.input_pos = 3.14
print("Position setpoint is " + str(my_drive.axis0.controller.pos_setpoint))

# And this is how function calls are done:
for i in [1,2,3,4]:
    print('voltage on GPIO{} is {} Volt'.format(i, my_drive.get_adc_voltage(i)))

calibrate_motor(my_drive.axis0)
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
# A sine wave to test
t0 = time.monotonic()
while True:
  
    SINE_PERIOD = 2.0
    t = time.monotonic() - t0
    phase = t * (2 * math.pi / SINE_PERIOD)
    setpoint = math.sin(phase)
    my_drive.axis0.controller.input_pos = setpoint
    time.sleep(0.01)

# Some more things you can try:

# Write to a read-only property:
my_drive.vbus_voltage = 11.0  # fails with `AttributeError: can't set attribute`

# Assign an incompatible value:
my_drive.motor0.pos_setpoint = "I like trains"  # fails with `ValueError: could not convert string to float`