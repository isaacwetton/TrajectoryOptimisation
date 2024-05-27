import pickle
from matplotlib import pyplot as plt
import numpy as np

# Load data
f = open("data/gam7data2.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, vels, Jdists = pickle.load(f)
f.close()

# Get data size
print(len(orbpos))

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

# Create plot
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (7, 5.5)
plt.rcParams["figure.dpi"] = 150
plt.plot(calxpos, calypos, "#c43e27")
plt.plot(ganxpos, ganypos, "#39667b")
plt.plot(ioxpos, ioypos, "#839435")
plt.plot(eurxpos, eurypos, "#e39c1b")
plt.plot(orbxpos, orbypos, "#342f29")
plt.scatter(0, 0, c="#342f29")
plt.legend(["Callisto", "Ganymede", "Io", "Europa", "Orbiter", "Jupiter"], loc="upper right", fontsize=12)

# plt.title("Orbiter trajectory shown in the XY plane for initial conditions\n"
#           r"$\delta = 4.653$, $\phi = -0.02744$, MJD = 59093.5")
plt.xlabel(r"X position ($\times$ 10$^{6}$ km)", fontsize=12)
plt.ylabel(r"Y position ($\times$ 10$^{6}$ km)", fontsize=12)

# plt.xlim([-1e6, 1.25e6])
# plt.ylim([-2.5e6, 0.5e6])
# plt.xticks(np.linspace(-1e6, 1.25e6, num=10, endpoint=True))
# plt.yticks(np.linspace(-2.5e6, 0.5e6, num=7, endpoint=True))
plt.xlim([-2.5e6, 2.5e6])
plt.ylim([-2.5e6, 2.5e6])
plt.xticks(np.linspace(-2.5e6, 2.5e6, num=11, endpoint=True))
plt.yticks(np.linspace(-2.5e6, 2.5e6, num=11, endpoint=True))
plt.gca().set_aspect("equal")
plt.show()
