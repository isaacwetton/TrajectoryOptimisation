import pickle
from matplotlib import pyplot as plt
import numpy as np

# Load data
f = open("data/gam3data1.dat", "rb")
xpos, ypos, times = pickle.load(f)
f.close()

Jdist = []
for i in range(len(xpos)):
    Jdist.append(np.sqrt(xpos[i] ** 2 + ypos[i] ** 2))

# Create plot
plt.plot(times, Jdist)
plt.title(r"A plot of best semi-major axis of Jupiter orbit against $\phi$")
plt.xlabel(r"$\phi$ (rad)")
plt.ylabel("Semi-major axis")
plt.show()
