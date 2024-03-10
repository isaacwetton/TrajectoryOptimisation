import pickle
import matplotlib.pyplot as plt
import constants

# Load data
f = open("data/gam7data2.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, vels, Jdists = pickle.load(f)
f.close()

# Create plot
plt.plot(Jdists, vels, "k")

plt.title("A plot of orbiter velocity as a function of orbiter-Jupiter distance")
plt.xlabel("Orbiter-Jupiter distance (km)")
plt.ylabel("Orbiter velocity (km/s)")
plt.xlim([0, 7e7])
plt.show()
