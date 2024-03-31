from __future__ import print_function

import odrive
from odrive.enums import *
import time
from pynput import keyboard
import math


class position_movements:
    ''' for the movements class, the odrive has to be '''
    def __init__(self, odrv):
        self.odrv = odrv

    def _set_ctrl_mode(self, mode: ControlMode = ControlMode.POSITION_CONTROL):
        ''' 
        Set the control mode.
        '''
        self.odrv.axis0.controller.config.control_mode = mode

    def move_to_position(self, position: float):
        ''' 
        Move to a specific position.
        '''
        self._set_ctrl_mode()
        self.odrv.axis0.controller.input_pos = position

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
        if self.odrv.axis0.disarm_reason != 0:
            print("Motor disarmed. Reason: " + str(self.odrv.axis0.disarm_reason))
            raise KeyboardInterrupt

    def move_like_a_watch(self):
        ''' 
        Move the motor like a watch.
        '''
        self._set_ctrl_mode()
        for i in range(60):
            self.odrv.axis0.controller.input_pos = i/60
            time.sleep(1)

            if self.odrv.axis0.disarm_reason != 0:
                print("Motor disarmed. Reason: " + str(self.odrv.axis0.disarm_reason))
                raise KeyboardInterrupt
        
class velocity_movements:

    def __init__(self, odrv):
        self.odrv = odrv

    def _set_ctrl_mode(self, mode: ControlMode = ControlMode.VELOCITY_CONTROL):
        ''' 
        Set the control mode.
        '''
        self.odrv.axis0.controller.config.control_mode = mode

    def vel_stop(self):
        ''' 
        Stop the motor.
        '''
        self.odrv.axis0.controller.input_vel = 0

    def pedal_controlled(self, velocity: float = 1):
        ''' 
        Pedal controlled movement.
        '''
        self._set_ctrl_mode()
        self.odrv.axis0.controller.input_vel = velocity

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


                elif self.odrv.axis0.disarm_reason != 0:
                    print("Motor disarmed. Reason: " + str(self.odrv.axis0.disarm_reason))
                    raise KeyboardInterrupt
                

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