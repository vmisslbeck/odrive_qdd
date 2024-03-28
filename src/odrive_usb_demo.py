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

def print_GPIO_voltage(odrv):
    ''' 
    Print the voltage on GPIO pinS.
    Input arguments look like this: my_drive (odrive object)
    '''
    for i in [1,2,3,4]:
        print('voltage on GPIO{} is {} Volt'.format(i, odrv.get_adc_voltage(i)))

def find_one_odrive():
    ''' 
    Find a connected ODrive (this will block until you connect one)
    '''
    print("finding an odrive...")
    odrv = odrive.find_any()
    print("Odrive found!")
    odrv.clear_errors()
    time.sleep(0.5)
    return odrv

def find_all_odrives():
    '''
    if you want to use more than one odrive
    to use the object, you can do this:
    my_drive0 = find_all_odrives()[0]
    '''
    #print(type(odrive.find_any())) # : <class 'fibre.libfibre.anonymous_interface_2380363422560'>

    # we use find_any because it will start a background thread that handles the backend,
    # so in the end we can access odrive.connected_devices
    odrive.find_any()
    od_list = []
    for i in range(len(odrive.connected_devices)):
        odrv = odrive.connected_devices[i]
        od_list.append(odrv)

    return od_list


my_drive = find_one_odrive()
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
