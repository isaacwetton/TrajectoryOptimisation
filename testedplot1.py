import pickle
import numpy as np
from matplotlib import pyplot as plt

# Load data
f = open("data/monte1test1.dat", "rb")
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
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["font.size"] = 13
plt.rcParams["figure.figsize"] = (7, 5.5)
plt.rcParams["figure.dpi"] = 150

plt.plot(x, y, "#342f29")
# plt.title("A plot of identified required propellants\nfor successive simulated annealing tests")
plt.xlabel(r"Test", fontsize=13)
plt.ylabel("Propellant required for capture (kg)", fontsize=13)
plt.show()
