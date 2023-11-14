import pickle
from matplotlib import pyplot as plt

# Load data
(x, y, z) = pickle.load("data/contour2data.dat")

# Create contour plot
fig = plt.figure()
contour = plt.contourf(x, y, z, 500)
cbar = plt.colorbar(contour)
cbar.set_label("Closest Approach to Callisto (km)")
plt.xlabel(r"Starting position, $\delta$ (rad)")
plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
plt.title(r"Contour plot of Closest Approach to Callisto (km) as a Function of $\delta$ and $\phi$")

plt.show()