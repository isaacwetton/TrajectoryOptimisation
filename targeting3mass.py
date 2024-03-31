import pickle
from matplotlib import pyplot as plt
import numpy as np
import constants

# Load data
f = open("data/targeting3data1.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, lats, lons, orbmass = pickle.load(f)
f.close()

print(orbmass[-1])
alats = np.array(lats, dtype=float)
alons = np.array(lons, dtype=float)
alats *= 360 / (2*np.pi)
alons *= 360 / (2*np.pi)

# Manipulate time
times = np.array(times, dtype=float)
x = (times - times[0]) / constants.DAY_IN_SECONDS

# Create red line for minimum allowed mass
xred = np.linspace(0, 350, num=50, endpoint=True)
yred = np.zeros(50) + 1000

# Create plot
fig = plt.figure()
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["figure.figsize"] = (8, 6)
plt.rcParams["figure.dpi"] = 200
plt.plot(x, orbmass, c="#342f29", label="Orbiter mass")
plt.plot(xred, yred, c="#c43e27", label="Minimum allowed mass")
# plt.title("Orbiter latitudes and longitudes with respect to Ganymede recorded\nwhen in valid Ganymede flyby altitude range")
plt.xlabel(r"Time (days)", fontsize=12)
plt.ylabel(r"Orbiter Mass (kg)", fontsize=12)
plt.xlim([0, 350])
plt.ylim([500, 2500])
# plt.ylim([-90, 90])
# plt.xticks(np.arange(-180, 210, step=30))
# plt.yticks(np.arange(-90, 105, step=15))
# plt.tick_params(axis='y', which='both', labelleft='on', labelright='on')
# ax.yaxis.set_ticks_position('both')
# plt.tick_params(axis='x', which='both', labeltop='on')
# ax.xaxis.set_ticks_position('both')
plt.legend(loc="upper right", fontsize=12)
plt.show()
