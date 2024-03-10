import pickle
import numpy as np
from matplotlib import pyplot as plt

# Load data
f = open("data/simannJup4tested1.dat", "rb")
tested = pickle.load(f)
f.close()

# Create y axis
y = []
for i in tested:
    output = i[-1]
    if output < 1e9:
        y.append(output)

# Create x axis
x = np.arange(1, len(y) + 1)

# Create plot
plt.plot(x, y, "k")
plt.title("A plot of identified required propellants for successive simulated annealing tests")
plt.xlabel(r"Test")
plt.ylabel("Mass of propellant required for ideal capture (kg)")
plt.show()
