from __future__ import print_function

import odrive
from odrive.enums import *
import time
import sys

class Utils:

    # BLDC Kv
    BLDC_KV = 90.0

    # Min/Max phase inductance of motor
    MIN_PHASE_INDUCTANCE = 0
    MAX_PHASE_INDUCTANCE = 0.001

    # Min/Max phase resistance of motor
    MIN_PHASE_RESISTANCE = 0
    MAX_PHASE_RESISTANCE = 0.5

    # Tolerance for encoder offset float
    ENCODER_OFFSET_FLOAT_TOLERANCE = 0.05

    # The different motor states are defined as variables, because the changed in the past already in form of naming
    closed_loop = AxisState.CLOSED_LOOP_CONTROL
    idle = AxisState.IDLE
    calibration_state = AxisState.MOTOR_CALIBRATION
    full_calibration_seq = AxisState.FULL_CALIBRATION_SEQUENCE
    encoder_offset = AxisState.ENCODER_OFFSET_CALIBRATION


    def _find_odrive(self):
        # connect to Odrive
        self.odrv = odrive.find_any(timeout=15)
        self.odrv_axis = getattr(self.odrv, "axis{}".format(self.axis_num))
        self.odrv_axis = self.odrv.axis0

    def find_one_odrive(self):
        ''' 
        Find a connected ODrive (this will block until you connect one)
        '''
        print("finding an odrive...")
        odrv = odrive.find_any()
        print("Odrive found!")
        odrv.clear_errors()
        time.sleep(0.5)
        time.sleep(1)
        odrv.clear_errors() # this clear_errors is critical, otherwise we always get ERRORS
        return odrv

    def find_all_odrives(self):
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

    def clear_errors(self):
        """
        Clears all errors on the odrive.
        """
        self.odrv.clear_errors()

    def settings(self):
        '''
        set the settings like you need it. The predefined settings will most likely not fit exactly for you system.
        '''
        # Set this to True if using a brake resistor
        self.odrv.config.dc_bus_overvoltage_trip_level = 30
        self.odrv.config.dc_bus_undervoltage_trip_level = 20
        self.odrv.config.dc_max_positive_current = 8
        # This is the amount of current allowed to flow back into the power supply.
        # The convention is that it is negative. By default, it is set to a
        # conservative value of 10mA. If you are using a brake resistor and getting
        # DC_BUS_OVER_REGEN_CURRENT errors, raise it slightly. If you are not using
        # a brake resistor and you intend to send braking current back to the power
        # supply, set this to a safe level for your power source. Note that in that
        # case, it should be higher than your motor current limit + current limit
        # margin.
        self.odrv.config.dc_max_negative_current = -0.01
        self.odrv.config.brake_resistor0.enable = True
        # This is the resistance of the brake resistor. You can leave this
        # at the default setting if you are not using a brake resistor. Note
        # that there may be some extra resistance in your wiring and in the
        # screw terminals, so if you are getting issues while braking you may
        # want to increase this parameter by around 0.05 ohm.
        self.odrv.config.brake_resistor0.resistance = 2
        self.odrv.axis0.config.motor.motor_type = MotorType.HIGH_CURRENT
        # Estimated KV but should be measured using the "drill test", which can
        # be found here:
        # https://discourse.odriverobotics.com/t/project-hoverarm/441
        self.odrv.axis0.config.motor.torque_constant = 8.27 / self.BLDC_KV # for EaglePower8308 90KV = 0.09188888888888888
        # Eagle Power 8308 BLDC has 40 Magnets,
        # so 40 poles, and thus 20 pole pairs
        self.odrv.axis0.config.motor.pole_pairs = 20
        self.odrv.axis0.config.motor.current_soft_max = 22
        self.odrv.axis0.config.motor.current_hard_max = 38.6
        self.odrv.axis0.config.motor.calibration_current = 4
        # the Eagle Power 8308 is an Agricultural Drone Motor, so it needs a high
        # voltage to get the calibration right. The resistance calibration is
        # particularly sensitive to the voltage, so we want to use a higher
        # voltage for the calibration. The resistance_calib_max_voltage is the
        # voltage that the ODrive will use to measure the resistance of the motor
        # windings. The default value is 1V, but we can increase it to 4V to get
        # a more accurate measurement. The resistance_calib_max_voltage should be
        # set to a value that is higher than the voltage that the motor will
        # actually see during operation.
        # The motors are also fairly high inductance, so we need to reduce the
        # bandwidth of the current controller from the default to keep it
        # stable.
        self.odrv.axis0.config.motor.resistance_calib_max_voltage = 5
        self.odrv.axis0.config.calibration_lockin.current = 4
        self.odrv.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
        self.odrv.axis0.controller.config.input_mode = InputMode.VEL_RAMP
        self.odrv.axis0.controller.config.vel_ramp_rate = 10
        self.odrv.axis0.controller.config.vel_limit = 12
        self.odrv.axis0.controller.config.vel_limit_tolerance = 1.1666666666666667
        self.odrv.axis0.config.torque_soft_min = -0.404
        self.odrv.axis0.config.torque_soft_max = 0.404

        # enable CAN communication
        self.odrv.can.config.protocol = Protocol.SIMPLE
        self.odrv.can.config.baud_rate = 250000
        self.odrv.axis0.config.can_node_id = 0
        self.odrv.axis0.config.can.heartbeat_rate_ms = 100
        self.odrv.axis0.config.can.encoder_msg_rate_ms = 10
        self.odrv.axis0.config.can.iq_msg_rate_ms = 10
        self.odrv.axis0.config.can.torques_msg_rate_ms = 10
        self.odrv.axis0.config.can.error_msg_rate_ms = 10
        self.odrv.axis0.config.can.temperature_msg_rate_ms = 10
        self.odrv.axis0.config.can.bus_voltage_msg_rate_ms = 10
        self.odrv.axis0.config.enable_watchdog = False

        # For the BLDC we use the onboard encoder on the back of the odrive.
        self.odrv.axis0.config.load_encoder = EncoderId.ONBOARD_ENCODER0
        self.odrv.axis0.config.commutation_encoder = EncoderId.ONBOARD_ENCODER0     

        # enable UART communication
        self.odrv.config.enable_uart_a = True
        self.odrv.config.gpio7_mode = GpioMode.UART_A
        self.odrv.config.gpio6_mode = GpioMode.UART_A
        self.odrv.config.uart_a_baudrate = 115200


    def configure_odrive(self):
        """
        Configures the odrive for a BLDC motor.
        """
        if self.erase_config:
            # Erase pre-exsisting configuration
            print("Erasing pre-exsisting configuration...")
            try:
                self.odrv.erase_configuration()
            except Exception:
                pass

        self._find_odrive()

        self.settings()

        # Set in position control mode so we can control the position of the
        # wheel
        self.odrv_axis.controller.config = ControlMode.POSITION_CONTROL

        # Motor must be in IDLE mode before saving
        self.odrv_axis.requested_state = self.idle
        try:
            print("Saving manual configuration and rebooting...")
            is_saved = self.odrv.save_configuration()
            if not is_saved:
                print("Error: Configuration not saved. Are all motors in IDLE state?")
            else:
                print("Calibration configuration saved.")

            print("Manual configuration saved.")
        except Exception as e:
            pass

        self._find_odrive()

        input("Make sure the motor is free to move, then press enter...")

        print("Calibrating Odrive for motor (you should hear a " "beep)...")

        self.odrv_axis.requested_state = self.calibration_state

        # Wait for calibration to take place
        time.sleep(15)

        if self.odrv_axis.motor.error != 0:
            print(
                "Error: Odrive reported an error of {} while in the state "
                "AXIS_STATE_MOTOR_CALIBRATION. Printing out Odrive motor data for "
                "debug:\n{}".format(self.odrv_axis.motor.error, self.odrv_axis.motor)
            )

            sys.exit(1)

        if (
            self.odrv_axis.motor.config.phase_inductance <= self.MIN_PHASE_INDUCTANCE
            or self.odrv_axis.motor.config.phase_inductance >= self.MAX_PHASE_INDUCTANCE
        ):
            print(
                "Error: After odrive motor calibration, the phase inductance "
                "is at {}, which is outside of the expected range. Either widen the "
                "boundaries of MIN_PHASE_INDUCTANCE and MAX_PHASE_INDUCTANCE (which "
                "is between {} and {} respectively) or debug/fix your setup. Printing "
                "out Odrive motor data for debug:\n{}".format(
                    self.odrv_axis.motor.config.phase_inductance,
                    self.MIN_PHASE_INDUCTANCE,
                    self.MAX_PHASE_INDUCTANCE,
                    self.odrv_axis.motor,
                )
            )

            sys.exit(1)

        if (
            self.odrv_axis.motor.config.phase_resistance <= self.MIN_PHASE_RESISTANCE
            or self.odrv_axis.motor.config.phase_resistance >= self.MAX_PHASE_RESISTANCE
        ):
            print(
                "Error: After odrive motor calibration, the phase resistance "
                "is at {}, which is outside of the expected range. Either raise the "
                "MAX_PHASE_RESISTANCE (which is between {} and {} respectively) or "
                "debug/fix your setup. Printing out Odrive motor data for "
                "debug:\n{}".format(
                    self.odrv_axis.motor.config.phase_resistance,
                    self.MIN_PHASE_RESISTANCE,
                    self.MAX_PHASE_RESISTANCE,
                    self.odrv_axis.motor,
                )
            )

            sys.exit(1)

        # If all looks good, then lets tell ODrive that saving this calibration
        # to persistent memory is OK
        self.odrv_axis.motor.config.pre_calibrated = True

        if self.odrv_axis.encoder.error != 0:
            print(
                "Error: Odrive reported an error of {} while in the state "
                "AXIS_STATE_ENCODER_HALL_POLARITY_CALIBRATION. Printing out Odrive encoder "
                "data for debug:\n{}".format(
                    self.odrv_axis.encoder.error, self.odrv_axis.encoder
                )
            )

            sys.exit(1)

        print("Calibrating Odrive for encoder offset...")
        self.odrv_axis.requested_state = self.encoder_offset

        # Wait for calibration to take place
        time.sleep(30)

        if self.odrv_axis.encoder.error != 0:
            print(
                "Error: Odrive reported an error of {} while in the state "
                "AXIS_STATE_ENCODER_OFFSET_CALIBRATION. Printing out Odrive encoder "
                "data for debug:\n{}".format(
                    self.odrv_axis.encoder.error, self.odrv_axis.encoder
                )
            )

            sys.exit(1)

        # If all looks good, then lets tell ODrive that saving this calibration
        # to persistent memory is OK
        self.odrv_axis.encoder.config.pre_calibrated = True

        print("Calibrating Odrive for anticogging...")
        self.odrv_axis.requested_state = self.closed_loop

        self.odrv_axis.controller.start_anticogging_calibration()

        while self.odrv_axis.controller.config.anticogging.calib_anticogging:
            time.sleep(15)
            print("Still calibrating anticogging...")

        if self.odrv_axis.controller.error != 0:
            print(
                "Error: Odrive reported an error of {} while performing "
                "start_anticogging_calibration(). Printing out Odrive controller "
                "data for debug:\n{}".format(
                    self.odrv_axis.controller.error, self.odrv_axis.controller
                )
            )

            sys.exit(1)

        # If all looks good, then lets tell ODrive that saving this calibration
        # to persistent memory is OK
        self.odrv_axis.controller.config.anticogging.pre_calibrated = True

        # Motors must be in IDLE mode before saving
        self.odrv_axis.requested_state = self.idle
        try:
            print("Saving calibration configuration and rebooting...")
            self.odrv.save_configuration()
            if not is_saved:
                print("Error: Configuration not saved. Are all motors in IDLE state?")
            else:
                print("Calibration configuration saved.")
        except Exception as e:
            pass

        self._find_odrive()

        print("Odrive configuration finished.")

    def calibrate_motor(self, motor):
        ''' 
        Calibrate motor and wait for it to finish.
        Input argument looks like this: odrive.axis0 
        '''
        print("Calibrating motor...")
        motor.requested_state = self.full_calibration_seq
        while motor.current_state != self.idle:
            time.sleep(0.1)
        print("Motor calibrated.")
        motor.requested_state = self.closed_loop

    def print_GPIO_voltage(self, odrv):
        ''' 
        Print the voltage on GPIO pins.
        Input arguments look like this: my_drive (odrive object)
        '''
        for i in [1,2,3,4]:
            print('voltage on GPIO{} is {} Volt'.format(i, odrv.get_adc_voltage(i)))

    def check_voltage(self, odrv, voltage:float =20.0):
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

    def check_errors(self, odrv, want_to_clear_errors: bool = False):
        ''' 
        Check if there are errors on the ODrive and clear them if necessary.
        Input arguments look like this: my_drive (odrive object), want_to_clear_errors (bool)
        '''
        odrv.utils.dump_errors(odrv, want_to_clear_errors)
        print(odrv.utils.dump_errors(odrv))
    