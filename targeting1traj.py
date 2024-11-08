import pickle
from matplotlib import pyplot as plt
import numpy as np

# Load data
f = open("data/targeting1data1.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, gan_map_lats, gan_map_lons = pickle.load(f)
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
plt.plot(calxpos, calypos, "red")
plt.plot(ganxpos, ganypos, "blue")
plt.plot(ioxpos, ioypos, "green")
plt.plot(eurxpos, eurypos, "yellow")
plt.plot(orbxpos, orbypos, "k")
plt.scatter(0, 0, c="k")
plt.legend(["Callisto", "Ganymede", "Io", "Europa", "Orbiter", "Jupiter"])

plt.title("Orbiter trajectory shown in the XY plane for initial conditions\n"
          r"$\delta = 4.653$, $\phi = -0.02744$, MJD = 59093.5")
plt.xlabel(r"X position (km)")
plt.ylabel("Y position (km)")
plt.show()
