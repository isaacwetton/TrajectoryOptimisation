import pickle
import constants
from matplotlib import pyplot as plt

# Load data
f = open("data/contour2data4.dat", "rb")
(x, y, z) = pickle.load(f)
f.close()

# Create contour plot
fig = plt.figure()
contour = plt.contourf(x, y, z - constants.R_CALLISTO, 1000)
cbar = plt.colorbar(contour)
cbar.set_label("Altitude at Closest Approach to Callisto (km)")
plt.xlabel(r"Starting position, $\delta$ (rad)")
plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
plt.title(r"Contour plot of Closest Approach Altitude at Callisto (km) as a Function of $\delta$ and $\phi$")

plt.show()
