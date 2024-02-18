import pickle
import constants
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches

# Load contour data
f = open("data/contour3data1.dat", "rb")
(x, y, closest_cal, closest_gan) = pickle.load(f)
f.close()
both = closest_cal + closest_gan
# Convert to degrees
x *= 360 / (2*np.pi)
y *= 360 / (2*np.pi)

# Load simann test data
f = open("data/simannJup2tested3.dat", "rb")
pre_tested = pickle.load(f)
tested = []
for i in pre_tested:
    pre_vals = i[0:2]
    vals = []
    for j in pre_vals:
        vals.append(j*(360 / (2*np.pi)))
    tested.append([*vals, i[2]])
f.close()

# Generate lists of evolving best solutions and worse solutions
deltas = []
phis = []
bad_deltas = []
bad_phis = []
best = -1e10
counter = 0
for i in tested:
    output = i[-1]
    if output >= 1e9:
        output = - (output - 1e9)

    if best < 0 and output > best:
        deltas.append(i[0])
        phis.append((i[1]))
        counter += 1
        best = output
        print(output)
    elif best > output > 0:
        deltas.append(i[0])
        phis.append((i[1]))
        counter += 1
        best = output
        print(output)
    elif output != -1e10:
        bad_deltas.append(i[0])
        bad_phis.append((i[1]))

print(counter)
# Create contour plot and line plot
fig = plt.figure()
contour = plt.contourf(x, y, both, 1000, cmap="cividis")
cbar = plt.colorbar(contour)
plt.scatter(bad_deltas, bad_phis, c="red", label="Tested worse solutions", s=10)
plt.plot(deltas, phis, "lime", label="Evolution of best solution")
ax = plt.gca()
rect = patches.Rectangle((0, -0.02 * (360 / (2*np.pi))), 2*np.pi*(360 / (2*np.pi)), 0.04 * (360 / (2*np.pi)), alpha=0.25, color="white")
ax.add_patch(rect)
plt.legend(loc="upper right")
cbar.set_label("Sum of closest approaches to Callisto and Ganymede (km)")
plt.xlabel(r"Starting position, $\delta$ ($\degree$)")
plt.xlim([0, 360])
plt.xticks(np.arange(0, 450, step=90))
plt.ylabel(r"Initial velocity direction, $\phi$ ($\degree$)")
plt.title("A plot of the evolution of the best solution within the search space\n"
          "for simulated annealing of the Jupiter capture")

plt.show()
