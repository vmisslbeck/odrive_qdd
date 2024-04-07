from __future__ import print_function

from odrive.enums import *
import time
from pynput import keyboard
import math


class position_movements:
    ''' for the movements class, the odrive has to be '''
    def __init__(self, odrv, gear_ratio_xto1: float = 1):
        self.odrv = odrv
        self.gear_ratio_xto1 = gear_ratio_xto1

    def _set_ctrl_mode(self, mode: ControlMode = ControlMode.POSITION_CONTROL):
        ''' 
        Set the control mode.
        '''
        self.odrv.axis0.controller.config.control_mode = mode

    def disarm_interrupt(self):
        '''
        checks if the motor is disarmed , prints the reason and raises a KeyboardInterrupt
        '''
        if self.odrv.axis0.disarm_reason != 0:
            print("Motor disarmed. Reason: " + str(self.odrv.axis0.disarm_reason))
            raise KeyboardInterrupt

    def move_to_position(self, position: float):
        ''' 
        Move to a specific position. Note that position can go from -inf to +inf. That is not the same as angle.
        '''
        self._set_ctrl_mode()
        self.odrv.axis0.controller.input_pos = position

        self.disarm_interrupt()

    def move_to_angle(self, angle: float):
        ''' 
        Move to a specific angle. Note that angle can go from 0 to 360 degrees.
        For example, if the motor is in encoder position 5000 and you want to move to angle 0, the motor won't move t0 encoder position 0, 
        but the nearest encoder position to angle 0.
        '''
        self._set_ctrl_mode()
        pos = float(self.odrv.axis0.controller.pos_setpoint)
        pos += angle * 8192 / 360 * self.gear_ratio_xto1
        self.odrv.axis0.controller.input_pos = pos
        #what is the 8192? it is the number of encoder counts per revolution
        #how do we know that? we can check it in the odrivetool by typing odrv0.axis0.encoder.config
        print(self.odrv.axis0.encoder.config) # test this!!!!

        self.disarm_interrupt()

    def sine_wave(self, t0: float, SINE_PERIOD: float = 2):
        ''' 
        A sine wave to eternity.
        the smaller the value of SINE_PERIOD, the faster the motor will spin
        '''
        self._set_ctrl_mode()
        t = time.monotonic() - t0
        phase = t * (2 * math.pi / SINE_PERIOD)
        setpoint = math.sin(phase)
        self.odrv.axis0.controller.input_pos = setpoint
        time.sleep(0.01)
        
        self.disarm_interrupt()

    def move_like_a_watch(self):
        ''' 
        Move the motor like a watch.
        '''
        self._set_ctrl_mode()
        for i in range(60):
            self.odrv.axis0.controller.input_pos = i/60
            time.sleep(1)

            self.disarm_interrupt()
        
class velocity_movements:

    def __init__(self, odrv):
        self.odrv = odrv

    def _set_ctrl_mode(self, mode: ControlMode = ControlMode.VELOCITY_CONTROL):
        ''' 
        Set the control mode.
        '''
        self.odrv.axis0.controller.config.control_mode = mode

    def disarm_interrupt(self):
        '''
        chechks if the motor is disarmed , prints the reason and raises a KeyboardInterrupt
        '''
        if self.odrv.axis0.disarm_reason != 0:
            print("Motor disarmed. Reason: " + str(self.odrv.axis0.disarm_reason))
            raise KeyboardInterrupt

    def vel_stop(self):
        ''' 
        Stop the motor.
        '''
        self.odrv.axis0.controller.input_vel = 0

    def vel_controlled(self, velocity: float = 1):
        ''' 
        velocity controlled movement. use this method to move the motor with a specific velocity.
        '''
        self._set_ctrl_mode()
        self.odrv.axis0.controller.input_vel = velocity

        self.disarm_interrupt()

    def control_by_input(self):
        """
        With this method you can control the odrive with your arrow keys.
        Press arrow_up to increase velocity, arrow_down to decrease velocity.
        """
        self._set_ctrl_mode()
        print("Press arrow_up to increase velocity, arrow_down to decrease velocity, q to quit: ")
        while True:
            with keyboard.Events() as events:
        # Block for as much as possible
                
                event = events.get(1e6)
                if event.key == keyboard.KeyCode.from_char('q'):
                    print("input over.")
                    break
                elif event.key == keyboard.Key.esc:
                    print("input over.")
                    break
                
                elif event.key == keyboard.Key.up:
                    self.odrv.axis0.controller.input_vel += 0.1
                elif event.key == keyboard.Key.down:
                    self.odrv.axis0.controller.input_vel -= 0.1
                elif event.key == keyboard.Key.space:
                    self.odrv.axis0.controller.input_vel = 0

                self.disarm_interrupt()
                

    def move_back_and_forth(self, duration:float , velocity: float = 1):
        ''' 
        Move back and forth.
        '''

        self._set_ctrl_mode()

        self.odrv.axis0.controller.input_vel = velocity
        time.sleep(duration/2)
        self.odrv.axis0.controller.input_vel = -velocity
        time.sleep(duration/2)
        self.odrv.axis0.controller.input_vel = 0