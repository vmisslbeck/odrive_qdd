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
    ''' 
    Calibrate motor and wait for it to finish.
    Input argument looks like this: odrive.axis0 
    '''
    print("Calibrating motor...")
    motor.requested_state = AxisState.FULL_CALIBRATION_SEQUENCE
    while motor.current_state != AxisState.IDLE:
        time.sleep(0.1)
    print("Motor calibrated.")
    motor.requested_state = AxisState.CLOSED_LOOP_CONTROL


# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
    # print(type(odrive.find_any())) # : <class 'fibre.libfibre.anonymous_interface_2380363422560'>
    # if you want to use more than one odrive, you can use the following code
    #odrive.find_any()
    #my_drive1 = odrive.connected_devices[0]
    #my_drive2 = odrive.connected_devices[1]
    #...
my_drive = odrive.find_any()
print("Odrive found!")
my_drive.clear_errors()
time.sleep(0.5)

print("Bus voltage is " + str(my_drive.vbus_voltage) + " V")
if my_drive.vbus_voltage < 20.0:
    print("vbus voltage is too low! Please connect a power supply to the ODrive")
    while my_drive.vbus_voltage < 20:
        time.sleep(2)
        print("...")

time.sleep(1)
my_drive.clear_errors() # this clear_errors is critical, otherwise we always get ERRORS
my_drive.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
print("setpoint: " + str(my_drive.axis0.controller.pos_setpoint))

time.sleep(1)
# And this is how function calls are done:
# for i in [1,2,3,4]:
#    print('voltage on GPIO{} is {} Volt'.format(i, my_drive.get_adc_voltage(i)))

# Calibrate motor and wait for it to finish
# calibrate_motor(my_drive.axis0)

# A sine wave to test
t0 = time.monotonic()
try:
    while True:
  
        SINE_PERIOD = 2 # the smaller this value, the faster the motor will spin
        t = time.monotonic() - t0
        phase = t * (2 * math.pi / SINE_PERIOD)
        setpoint = math.sin(phase)
        my_drive.axis0.controller.input_pos = setpoint
        time.sleep(0.01)

except KeyboardInterrupt:
    my_drive.axis0.requested_state = AxisState.IDLE
    print("Motor stopped.")
    pass
