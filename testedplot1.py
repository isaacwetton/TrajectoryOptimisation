import pickle
import numpy as np
from matplotlib import pyplot as plt

# Load data
f = open("data/simannJup1tested1.dat", "rb")
tested = pickle.load(f)
f.close()

# Create y axis
y = []
for i in tested:
    output = i[-1]
    if output >= 1e9:
        y.append(-1*(output - 1e9))
    elif output > -1e10:
        y.append(output)

# Create x axis
x = np.arange(1, len(y) + 1)

# Create plot
plt.plot(x, y, "k")
plt.title("A plot of identified semi-major axes for successive simulated annealing tests")
plt.xlabel(r"Test")
plt.ylabel("Final semi-major axis of test (km)")
plt.show()
