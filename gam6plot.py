import pickle
import matplotlib.pyplot as plt
import constants

# Load data
f = open("data/gam6data1.dat", "rb")
Jdists, vels = pickle.load(f)
f.close()

# Create plot
plt.plot(Jdists, vels, "k")

plt.title("A plot of orbiter velocity as a function of orbiter-Jupiter distance")
plt.xlabel("Orbiter-Jupiter distance (km)")
plt.ylabel("Orbiter velocity (km/s)")
plt.xlim([0, 8e7])
plt.show()
