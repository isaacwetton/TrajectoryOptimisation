import pickle
import constants
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.animation import FFMpegWriter

# Load trajectory data
f = open("data/gam7data2.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, vels, Jdists = pickle.load(f)
f.close()

# Get orbiter x and y positions
orbxpos = []
orbypos = []
for pos in orbpos:
    orbxpos.append(pos[0])
    orbypos.append(pos[1])

# Get Callisto x and y positions
calxpos = []
calypos = []
for pos in calpos:
    calxpos.append(pos[0])
    calypos.append(pos[1])

ganxpos = []
ganypos = []
for pos in ganpos:
    ganxpos.append(pos[0])
    ganypos.append(pos[1])

eurxpos = []
eurypos = []
for pos in eurpos:
    eurxpos.append(pos[0])
    eurypos.append(pos[1])

ioxpos = []
ioypos = []
for pos in iopos:
    ioxpos.append(pos[0])
    ioypos.append(pos[1])

# Create figure
fig = plt.figure(figsize=(8, 6))


# Animation function
def animate(frame):
    global orbpos, calpos, ganpos, iopos, eurpos

    # Set up plot
    fig.clf()
    ax = fig.add_subplot()
    # ax.set_xlabel()
    # ax.set_ylabel()
    # ax.set_title()

    i = frame*10
    # Plot orbiter
    if 0 < i < 100:
        ax.plot(orbxpos[0:i], orbypos[0:i], label="Orbiter", c="k")
    elif i > 100:
        ax.plot(orbxpos[i-100:i], orbypos[i-100:i], label="Orbiter", c="k")

    # Plot Callisto
    if 0 < i < 100:
        ax.plot(calxpos[0:i], calypos[0:i], label="Callisto", c="red")
    elif i > 100:
        ax.plot(calxpos[i - 100:i], calypos[i - 100:i], label="Callisto", c="red")

    # Plot Ganymede
    if 0 < i < 100:
        ax.plot(ganxpos[0:i], ganypos[0:i], label="Ganymede", c="blue")
    elif i > 100:
        ax.plot(ganxpos[i - 100:i], ganypos[i - 100:i], label="Ganymede", c="blue")

    # Plot Io
    if 0 < i < 100:
        ax.plot(ioxpos[0:i], ioypos[0:i], label="Io", c="green")
    elif i > 100:
        ax.plot(ioxpos[i - 100:i], ioypos[i - 100:i], label="Io", c="green")

    # Plot Europa
    if 0 < i < 100:
        ax.plot(eurxpos[0:i], eurypos[0:i], label="Europa", c="yellow")
    elif i > 100:
        ax.plot(eurxpos[i - 100:i], eurypos[i - 100:i], label="Europa", c="yellow")

    # Add legend
    ax.legend(loc="upper right")


# Run animation
ani = FuncAnimation(fig, animate, repeat=True,
                    frames=len(orbpos), interval=1)

plt.show()

# # Save animation as .gif file
# writer = PillowWriter(fps=30,
#                       metadata=dict(),
#                       bitrate=1800
#                       )
# ani.save('Plots + Animations/contour3ani.gif', writer=writer)

# # Save animation as .mp4 file
# writer = FFMpegWriter(fps=60)
# ani.save('Plots + Animations/contour3ani.mp4', writer=writer)
