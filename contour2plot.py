import pickle
import constants
import matplotlib.ticker as tck
from matplotlib import pyplot as plt
import numpy as np

# Load data
f = open("data/contour2data5.dat", "rb")
(x, y, z) = pickle.load(f)
f.close()

pi = np.pi

# Create contour plot
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (7, 5.5)
plt.rcParams["figure.dpi"] = 150

fig = plt.figure()
contour = plt.contourf(x, y, z - constants.R_CALLISTO, 1000, cmap="cividis")
cbar = plt.colorbar(contour)
cbar.set_label(r"Altitude at Closest Approach to Callisto ($\times$ 10$^{7}$ km)")
plt.xlabel(r"Starting position, $\delta$ (rad)")
plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
# plt.title(r"Contour plot of Closest Approach Altitude at Callisto (km) as a Function of $\delta$ and $\phi$")
plt.xlim([0, 2*pi])
plt.ylim([-pi/4, pi/4])
xticks = ["0", r"$\frac{π}{4}$", r"$\frac{π}{2}$", r"$\frac{3π}{4}$", r"$π$", r"$\frac{5π}{4}$", r"$\frac{3π}{2}$", r"$\frac{7π}{4}$", r"$2π$"]
yticks = [r"$-\frac{π}{4}$", r"$-\frac{3π}{16}$", r"$-\frac{π}{8}$", r"$-\frac{π}{16}$", "0", r"$\frac{π}{16}$", r"$\frac{π}{8}$", r"$\frac{3π}{16}$", r"$\frac{π}{4}$"]
plt.xticks(np.linspace(0, 2*pi, num=9, endpoint=True), xticks)
plt.yticks(np.linspace(-pi/4, pi/4, num=9, endpoint=True), yticks)

plt.show()
