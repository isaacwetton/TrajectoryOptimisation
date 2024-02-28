import pickle
import constants
from matplotlib import pyplot as plt

# Load data
f = open("data/contour3data2.dat", "rb")
(x, y, closest_cal, closest_gan) = pickle.load(f)
f.close()

both = closest_cal + closest_gan
grav_cal = constants.MU_CALLISTO / (closest_cal ** 2)
grav_gan = constants.MU_GANYMEDE / (closest_gan ** 2)
both_grav = grav_cal + grav_gan

# Create contour plot
fig = plt.figure()
contour = plt.contourf(x, y, both_grav, 1000, cmap="cividis")
cbar = plt.colorbar(contour)
cbar.set_label("Sum of maximum gravitational acceleration contribution\n"
               "magnitudes from Callisto and Ganymede (kms$^{-2}$)")
plt.xlabel(r"Starting position, $\delta$ (rad)")
plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
plt.title("Contour plot of the sum of maximum gravitational acceleration contributions from Callisto\nand "
          r"Ganymede centres (kms$^{-2}$)"
          r" as a function of $\delta$ and $\phi$")

plt.show()
