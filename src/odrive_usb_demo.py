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

def check_voltage(odrv, voltage:float =20.0):
    ''' 
    Check if the voltage is high enough to run the motor.
    Input argument looks like this: my_drive (odrive object), voltage (float)
    '''
    print("Bus voltage is " + str(odrv.vbus_voltage) + " V")
    if odrv.vbus_voltage < voltage:
        print("vbus voltage is too low! Please connect a power supply to the ODrive")
        while odrv.vbus_voltage < voltage:
            time.sleep(2)
            print("...")


class movements:
    ''' for the movements class, the odrive has to be '''
    def __init__(self, odrv):
        self.odrv = odrv
        odrv.axis0.controller.config.control_mode = ControlMode.POSITION_CONTROL

    def sine_wave(self, t0: float, SINE_PERIOD: float = 2):
        ''' 
        A sine wave to eternity.
        the smaller the value of SINE_PERIOD, the faster the motor will spin
        '''
        t = time.monotonic() - t0
        phase = t * (2 * math.pi / SINE_PERIOD)
        setpoint = math.sin(phase)
        self.odrv.axis0.controller.input_pos = setpoint
        time.sleep(0.01)
        if self.odrv.axis0.disarm_reason != 0:
            print("Motor disarmed. Reason: " + str(self.odrv.axis0.disarm_reason))
            raise KeyboardInterrupt

    def move_like_a_watch(self):
        ''' 
        Move the motor like a watch.
        '''
        for i in range(60):
            self.odrv.axis0.controller.input_pos = i/60
            time.sleep(1)

            if self.odrv.axis0.disarm_reason != 0:
                print("Motor disarmed. Reason: " + str(self.odrv.axis0.disarm_reason))
                raise KeyboardInterrupt
        

my_drive = find_one_odrive()
check_voltage(my_drive)

time.sleep(1)
my_drive.clear_errors() # this clear_errors is critical, otherwise we always get ERRORS
my_drive.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL
print("setpoint: " + str(my_drive.axis0.controller.pos_setpoint))

time.sleep(1)

# A sine wave to test
move = movements(my_drive)
t0 = time.monotonic()
try:
    while True:
  
        move.sine_wave(t0)

except KeyboardInterrupt:
    my_drive.axis0.requested_state = AxisState.IDLE
    print("Motor stopped.")
    pass
