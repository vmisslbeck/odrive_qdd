#!/usr/bin/env python3
"""
Example usage of the ODrive python library to monitor and control ODrive devices
"""

from __future__ import print_function
from odrive.enums import *
import time
import threading
import odrv_movements as mvmts
import odrv_con_and_calib as concal
import odrv_plot as oplot

cc = concal.Utils()

my_drive = cc.find_one_odrive()
cc.check_voltage(my_drive)

# my_drive.clear_errors() # this clear_errors is critical, otherwise we always get ERRORS
my_drive.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL

gear_ratio_x_to_1 = 9  # set this to the gear ratio of your motor, if no gear, set it to 1
move = mvmts.position_movements(my_drive, gear_ratio_x_to_1)
vel_move = mvmts.velocity_movements(my_drive)
plt = oplot.PlotMe(my_drive, gear_ratio_x_to_1)

print("setpoint: " + str(my_drive.axis0.controller.pos_setpoint))
print("encoder pos: " + str(move.get_rel_pos()))

time.sleep(1)


def control():
    vel_move.control_by_input()


# Erstelle und starte Control-Thread
control_thread = threading.Thread(target=control)
control_thread.start()

# Plotten im Hauptthread
t0 = time.monotonic()
try:
    plt.plot_circle_pos()

    while True:
        # Eine Sinuswelle zum Testen
        move.sine_wave(t0)

  
except KeyboardInterrupt:
    my_drive.axis0.requested_state = AxisState.IDLE
    print("Ctrl + C pressed. Motor stopped.")
    pass

# Warte auf den Control-Thread
control_thread.join()