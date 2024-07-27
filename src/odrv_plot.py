import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation
import numpy as np
import odrv_con_and_calib as concal
import odrv_movements as mvm

class PlotMe:
    def __init__(self, odrv, gear_ratio_xto1: float = 1):
        self.odrv = odrv
        self.mvmts = mvm.position_movements(odrv, gear_ratio_xto1)
        
        self.line = None

    def plot_position(self):
        '''Plot the position of the motor over time'''

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xs = []
        ys = []

        def animate(i, xs, ys):
            pos = round(self.mvmts.get_rel_pos(), 5)

            xs.append(len(xs))
            ys.append(pos)

            xs = xs[-1000:]
            ys = ys[-1000:]

            ax.clear()
            ax.plot(xs, ys)

            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Rotational Position over Time')
            plt.ylabel('turns')
            plt.xlabel('time')

        ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10, cache_frame_data=False)
        plt.show()

    def plot_circle_pos(self):
        '''Plot the position of the motor on a circle'''

        def get_sensor_angle():
            '''Get the angle of the sensor in degrees'''
            pos = self.mvmts.get_rel_pos_modulo_one()
            deg = pos * 360
            return deg


   
        def update(frame):
            angle = get_sensor_angle()
            angle = -angle  # Invertiere den Winkel, um die Bewegung des Plots zu invertieren
            # Objekt aktueller Untersuchung!!!! wie könnte man es noch lösen, anstatt ein minus vor den angle
            # Aktualisiere den Titel des Plots mit dem neuen Winkel
            ax.set_title(f"Winkel: {-angle:.2f} Grad")

            # Lösche vorherige Linien und Punkte
            if self.line is not None:
                self.line.remove()
            # Konvertiere den Winkel von Grad in Bogenmaß
            angle_rad = np.deg2rad(angle)

            # Koordinaten für den Punkt auf dem Kreisrand
            x = np.cos(angle_rad)
            y = np.sin(angle_rad)

            # Zeichne den neuen Winkelpunkt
            #ax.plot([0, x], [0, y], marker='o', color='red')
            self.line, = ax.plot([0, x], [0, y], marker='o', color='red')

        # Erstellen des Kreises
        circle = plt.Circle((0, 0), 1, color='blue', fill=False)

        # Erstellen der Abbildung und der Achsen
        fig, ax = plt.subplots()

        # Kreis hinzufügen
        ax.add_artist(circle)

        # Achsenverhältnisse gleich setzen und Limiten festlegen
        ax.set_aspect('equal')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)

        # Gitternetz anzeigen
        plt.grid(True)

        # Animation erstellen
        ani = FuncAnimation(fig, update, interval=100, cache_frame_data=False)  # Interval in Millisekunden

        # Live-Plot anzeigen
        plt.show()

gear_ratio = 9
cc = concal.Utils()
my_drive = cc.find_one_odrive()
my_plot = PlotMe(my_drive, 9)

#my_plot.plot_position()
my_plot.plot_circle_pos()