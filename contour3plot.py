import pickle
import constants
from matplotlib import pyplot as plt

# Load data
f = open("data/contour3data1.dat", "rb")
(x, y, closest_cal, closest_gan) = pickle.load(f)
f.close()

both = closest_cal + closest_gan

# Create contour plot
fig = plt.figure()
contour = plt.contourf(x, y, closest_cal - constants.R_CALLISTO, 1000)
cbar = plt.colorbar(contour)
cbar.set_label("Altitude at closest approach to Callisto (km)")
plt.xlabel(r"Starting position, $\delta$ (rad)")
plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
plt.title(r"Contour plot of closest approach altitude at Callisto (km) as a function of $\delta$ and $\phi$")

plt.show()
