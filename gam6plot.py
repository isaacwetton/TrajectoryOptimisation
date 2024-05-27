import pickle
import matplotlib.pyplot as plt
import numpy as np
import constants

# Load data
f = open("data/gam7data3.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, vels, Jdists = pickle.load(f)
f.close()

# Create plot
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (7, 5.5)
plt.rcParams["figure.dpi"] = 150

# Io
io = [np.zeros(50) + 442e3, np.linspace(0, 45, endpoint=True)]
plt.plot(*io, "#839435", lw=1.0)
# Europa
eur = [np.zeros(50) + 617e3, np.linspace(0, 45, endpoint=True)]
plt.plot(*eur, "#e39c1b", lw=1.0)
# Ganymede
gan = [np.zeros(50) + 1070e3, np.linspace(0, 45, endpoint=True)]
plt.plot(*gan, "#39667b", lw=1.0)
# Callisto
cal = [np.zeros(50) + 1880e3, np.linspace(0, 45, endpoint=True)]
plt.plot(*cal, "#c43e27", lw=1.0)

plt.plot(Jdists, vels, "#342f29", label="Orbiter velocity")

# plt.title("A plot of orbiter velocity as a function of orbiter-Jupiter distance")
plt.xlabel(r"Orbiter-Jupiter distance ($\times$ 10$^{6}$ km)")
plt.ylabel("Orbiter velocity (km/s)")
plt.xlim([0, 2e6])
plt.ylim([0, 45])
plt.show()
