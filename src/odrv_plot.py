import matplotlib.pyplot as plt
import matplotlib.animation as animation
import odrv_con_and_calib as concal
import odrv_movements as mvm

class PlotMe:
    def __init__(self, odrv):
        self.odrv = odrv
        self.mvmts = mvm.BaseMovements(odrv)

    def plot_position(self):
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


cc = concal.Utils()
my_drive = cc.find_one_odrive()

PlotMe(my_drive).plot_position()