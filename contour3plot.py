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
contour = plt.contourf(x, y, both, 1000)
cbar = plt.colorbar(contour)
cbar.set_label("Sum of closest approaches to Callisto and Ganymede (km)")
plt.xlabel(r"Starting position, $\delta$ (rad)")
plt.ylabel(r"Initial velocity direction, $\phi$ (rad)")
plt.title("Contour plot of the sum of closest approaches to Callisto\nand Ganymede centres (km)"
         r" as a function of $\delta$ and $\phi$")

plt.show()
