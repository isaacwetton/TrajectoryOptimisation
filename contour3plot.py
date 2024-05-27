import pickle
import constants
from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

# Load data
f = open("data/contour3data6.dat", "rb")
(x, y, closest_cal, closest_gan) = pickle.load(f)
f.close()

both = closest_cal + closest_gan
grav_cal = constants.MU_CALLISTO / (closest_cal ** 2)
grav_gan = constants.MU_GANYMEDE / (closest_gan ** 2)
both_grav = grav_cal + grav_gan
minimum = []

for i in range(len(closest_cal)):
    minrow = []
    for j in range(len(closest_cal[i])):
        if closest_cal[i][j] < closest_gan[i][j]:
            minrow.append(closest_cal[i][j])
        else:
            minrow.append(closest_gan[i][j])
    minimum.append(minrow)

# # Create contour plot
# fig = plt.figure()
# contour = plt.contourf(x, y, both_grav, 1000, cmap="cividis")
# cbar = plt.colorbar(contour)
# cbar.set_label("Sum of maximum gravitational acceleration contribution\n"
#                "magnitudes from Callisto and Ganymede (kms$^{-2}$)")
# plt.xlabel(r"Starting position, $\delta$ (rad)")
# plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
# plt.title("Contour plot of the sum of maximum gravitational acceleration contributions from Callisto\nand "
#           r"Ganymede centres (kms$^{-2}$)"
#           r" as a function of $\delta$ and $\phi$ for initial time 59222.05 MJD")

# Create contour plot
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (7, 5.5)
plt.rcParams["figure.dpi"] = 150


fig = plt.figure()
contour = plt.contourf(x, y, minimum, 1000, cmap="cividis")
cbar = plt.colorbar(contour)
cbar.set_label("Minimum closest approach distance to\neither Callisto or "
               r"Ganymede centres ($\times$ 10$^{6}$ km)")
plt.xlabel(r"Starting position, $\delta$ (rad)")
plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
# plt.title("Contour plot of the sum of closest approach distances to Callisto and\nGanymede centres"
#           r" as a function of $\delta$ and $\phi$ for initial time 59222.05 MJD")
xticks = ["0", r"$\frac{π}{4}$", r"$\frac{π}{2}$", r"$\frac{3π}{4}$", r"$π$", r"$\frac{5π}{4}$", r"$\frac{3π}{2}$", r"$\frac{7π}{4}$", r"$2π$"]
pi = np.pi
plt.xticks(np.linspace(0, 2*pi, num=9, endpoint=True), xticks)
ax = plt.gca()
rect = patches.Rectangle((4, -0.04), 1, 0.02, alpha=1, color="white", fill=None)
ax.add_patch(rect)

plt.show()
