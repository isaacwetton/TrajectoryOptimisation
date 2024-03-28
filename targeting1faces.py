import pickle
from matplotlib import pyplot as plt
import numpy as np

# Load data
f = open("data/targeting2data2.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, lats, lons = pickle.load(f)
f.close()


alats = np.array(lats, dtype=float)
alons = np.array(lons, dtype=float)
alats *= 360 / (2*np.pi)
alons *= 360 / (2*np.pi)

# Create plot
fig = plt.figure()
img = plt.imread("Plots + Animations/GanymedeSurfaceFaces.png")
ax = fig.add_subplot(111)
ax.imshow(img, extent=[-180, 180, -90, 90])
plt.scatter(alons, alats, c="r", s=1)
plt.title("Orbiter latitudes and longitudes with respect to Ganymede recorded\nwhen in valid Ganymede flyby altitude range")
plt.xlabel(r"Longitude ($\degree$)")
plt.ylabel(r"Latitude ($\degree$)")
plt.xlim([-180, 180])
plt.ylim([-90, 90])
plt.xticks(np.arange(-180, 210, step=30))
plt.yticks(np.arange(-90, 105, step=15))
plt.tick_params(axis='y', which='both', labelleft='on', labelright='on')
ax.yaxis.set_ticks_position('both')
plt.tick_params(axis='x', which='both', labeltop='on')
ax.xaxis.set_ticks_position('both')
plt.show()
