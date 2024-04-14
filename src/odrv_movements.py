from __future__ import print_function

from odrive.enums import *
import time
from pynput import keyboard
import math

class BaseMovements:
    ''' The BaseMovements class is the parent class of the PositionMovements and VelocityMovements classes. It contains
    methods that are common to both classes.'''
    def __init__(self, odrv):
        self.odrv = odrv

    def _set_ctrl_mode(self, mode: ControlMode, input_mode: InputMode = InputMode.PASSTHROUGH):
        ''' 
        Set the control mode.
        '''
        self.odrv.axis0.controller.config.control_mode = mode
        self.odrv.axis0.controller.config.input_mode = input_mode

    def disarm_interrupt(self):
        '''
        checks if the motor is disarmed , prints the reason and raises a custom exception
        Look up Error codes here: https://docs.odriverobotics.com/v/latest/fibre_types/com_odriverobotics_ODrive.html#ODrive.Error
        '''
        if self.odrv.axis0.disarm_reason != 0:
            raise MotorDisarmedException(str(self.odrv.axis0.disarm_reason))
        
    def get_rel_pos(self):
        ''' 
        Get the relative position. Relative position is the position of the motor relative to the encoder position at startup.
        So if the motor makes 100 and a half turns, the relative position would be 100.5 and if you then turn it 200 truns in 
        the other direction, the relative position would be -99.5.
        '''
        # that method is kinda ugly, because the api is kinda clunky and there are so many
        # position variable but they all mean something else, for example odrv.axis0.commuation_mapper.pos_rel 
        # will never be greater than 1 or negative. If it is at 0.99 and you turn the motor 0.02 turns, it will be 0.01
        # so note, that the returned element could also be 'self.odrv.axis0.encoder.pos_estimate' 
        # (which you could think from reading the docs but I just can't find it and get errors when using it. 
        # Even in the odrive GUI inspector it is greyed out.)

        return self.odrv.axis0.pos_vel_mapper.pos_rel
    
    def get_rel_pos_modulo_one(self):
        '''Implement! not sure if you should use odrv.axis0.commuation_mapper.pos_rel or pos.abs or something else'''
        pass
    

class position_movements(BaseMovements):
    ''' the PositionMovements class is a subclass of the BaseMovements class. It handles
    all movements that are related to position control. typical Robot movements are position controlled.'''

    def __init__(self, odrv, gear_ratio_xto1: float = 1, circular_sector: list = [0, 360]):
        '''
        about circular_sector: if your motor should only move in a certain sector, you can define it here.
        if it can move 360 degrees, you can leave it as it is. If you want to move it only from 0 to 180 degrees,
        then the motor will never be in the sector from 180.1 to 360 degrees.
        You may wonder if the encoder position will be the same, when odrive is powered off and on again.
        '''
        self.odrv = odrv
        self.gear_ratio_xto1 = gear_ratio_xto1
        self.circular_sector = circular_sector
        self.controlMode = ControlMode.POSITION_CONTROL
        
    def dead_zone_guard(self, set_position: float):
        ''' 
        Guard the dead zone. The dead zone is the sector where the motor should not move.
        The odrive python api has hidden a absolute and relative position under odrv0.axis0.commutation_mapper.
        '''
        if self.circular_sector == [0, 360]:
            pass
        else:
            absolute_is_pos = self.odrv.axis.pos_estimate #absolute_is_pos = float(self.odrv.axis0.controller.pos_setpoint)
            relative_is_pos = self.odrv.axis0.commutation_mapper.pos_abs
            # Note, that the relative_is_pos is relaltive to one turn, you could say, if you multiply it by 360 it is an angle
            # but the odrive commutation_mapper absolute position (from above) is the same as described here. But the odrive
            # commutation_mapper relative position is realtive to the encoder postion at startup. So if the motor is turned 90 
            # degrees since startup (motor turned a quarter circle) then commutation_mapper.pos_rel would be about 0.25

            absolute_set_pos = set_position
            relative_set_pos = absolute_set_pos % 1

            if self.circular_sector[0] <= relative_set_pos*360 <= self.circular_sector[1]: #
                return set_position
            elif self.circular_sector[0] >= relative_set_pos*360:
                return int(absolute_is_pos) + (self.circular_sector[0]/360)
            elif self.circular_sector[1] <= relative_set_pos*360:
                return int(absolute_is_pos) + (self.circular_sector[1]/360)
            else:
                return self.odrv.axis0.encoder.pos_estimates
        
    def move_to_zero(self):
        ''' 
        Move to encoder position 0.
        '''
        self._set_ctrl_mode(self.controlMode)
        self.odrv.axis0.controller.input_pos = 0

        self.disarm_interrupt()

    def move_to_position(self, position: float):
        ''' 
        Move to a specific position. Note that position can go from -inf to +inf. That is not the same as angle.
        '''
        self._set_ctrl_mode(self.controlMode)
        self.odrv.axis0.controller.input_pos = position

        self.disarm_interrupt()

    def move_to_angle(self, angle: float):
        ''' 
        Move to a specific angle. Note that angle can go from 0 to 360 degrees.
        For example, if the motor is in encoder position 5000 and you want to move to angle 0, 
        the motor won't move to encoder position 0, but the nearest encoder position to angle 0.
        '''
        self._set_ctrl_mode(self.controlMode)
        pos = float(self.get_rel_pos())
        angle_in_float = angle/360
        x = angle_in_float - (pos%1)
        pos += x
        self.odrv.axis0.controller.input_pos = pos

        self.disarm_interrupt()

    def sine_wave(self, t0: float, sine_period: float = 2):
        ''' 
        A sine wave to eternity.
        the smaller the value of SINE_PERIOD, the faster the motor will spin
        '''
        self._set_ctrl_mode(self.controlMode)
        t = time.monotonic() - t0
        phase = t * (2 * math.pi / sine_period)
        setpoint = math.sin(phase)
        self.odrv.axis0.controller.input_pos = setpoint
        time.sleep(0.01)
        
        self.disarm_interrupt()

    def move_like_a_watch(self):
        ''' 
        Move the motor like a watch.
        '''
        self._set_ctrl_mode(self.controlMode)
        for i in range(60):
            self.odrv.axis0.controller.input_pos = i/60
            time.sleep(1)

            self.disarm_interrupt()
        
class velocity_movements(BaseMovements):
    ''' the VelocityMovements class is a subclass of the BaseMovements class. It handles 
    all movements that are related to velocity control. a typical example is a conveyor belt. or 
    a drone motor.'''

    def __init__(self, odrv):
        self.odrv = odrv
        self.controlMode = ControlMode.VELOCITY_CONTROL

    def vel_stop(self):
        ''' 
        Stop the motor.
        '''
        self.odrv.axis0.controller.input_vel = 0

    def vel_controlled(self, velocity: float = 1):
        ''' 
        velocity controlled movement. use this method to move the motor with a specific velocity.
        '''
        self._set_ctrl_mode(self.controlMode)
        self.odrv.axis0.controller.input_vel = velocity

        self.disarm_interrupt()

    def control_by_input(self):
        """
        With this method you can control the odrive with your arrow keys.
        Press arrow_up to increase velocity, arrow_down to decrease velocity.
        """
        self._set_ctrl_mode(self.controlMode)
        print("Press 'W' to increase velocity, 'S' to decrease velocity, q to quit: ")
        while True:
            with keyboard.Events() as events:
        # Block for as much as possible
                
                event = events.get(1e6)
                if event.key == keyboard.KeyCode.from_char('q') or event.key == keyboard.Key.esc:
                    print("input over.")
                    break
                
                elif event.key == keyboard.KeyCode.from_char('w'):
                    self.odrv.axis0.controller.input_vel += 0.1
                elif event.key == keyboard.KeyCode.from_char('s'):
                    self.odrv.axis0.controller.input_vel -= 0.1
                elif event.key == keyboard.Key.space:
                    self.odrv.axis0.controller.input_vel = 0

                self.disarm_interrupt()
                

    def move_back_and_forth(self, duration:float , velocity: float = 1):
        ''' 
        Move back and forth.
        '''

        self._set_ctrl_mode(self.controlMode)

        self.odrv.axis0.controller.input_vel = velocity
        time.sleep(duration/2)
        self.odrv.axis0.controller.input_vel = -velocity
        time.sleep(duration/2)
        self.odrv.axis0.controller.input_vel = 0


class MotorDisarmedException(Exception):
    '''class for custom exception for motor controller'''
    def __init__(self, message):
        self.reason = message
        super().__init__(f"Motor disarmed. Reason: {self.reason}")