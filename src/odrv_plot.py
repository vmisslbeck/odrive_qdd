import matplotlib.pyplot as plt
import matplotlib.animation as animation
import odrv_con_and_calib as concal
import odrv_movements as mvm

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

# Initialize odrive
cc = concal.Utils()
my_drive = cc.find_one_odrive()
mvmts = mvm.BaseMovements(my_drive)

def animate(i, xs, ys):


    pos = round(mvmts.get_rel_pos(), 5)

    # Add x and y to lists
    xs.append(len(xs))
    ys.append(pos)

    # Limit x and y lists to 1000 items #choose how many values you want to see
    xs = xs[-1000:]
    ys = ys[-1000:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Rotational Position over Time')
    plt.ylabel('turns')
    plt.xlabel('time')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=10, cache_frame_data=False)
plt.show()