import pickle
import constants
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches

# Load contour data
f = open("data/contour3data6.dat", "rb")
(x, y, closest_cal, closest_gan) = pickle.load(f)
f.close()
both = closest_cal + closest_gan
minimum = []
for i in range(len(closest_cal)):
    minrow = []
    for j in range(len(closest_cal[i])):
        if closest_cal[i][j] < closest_gan[i][j]:
            minrow.append(closest_cal[i][j])
        else:
            minrow.append(closest_gan[i][j])
    minimum.append(minrow)

# Convert to degrees
x *= 360 / (2*np.pi)
y *= 360 / (2*np.pi)

# Load simann test data
# f = open("data/monte1test1.dat", "rb")
f = open("data/monte1test1.dat", "rb")
pre_tested = pickle.load(f)
print(pre_tested)
tested = []
for i in pre_tested:
    pre_vals = i[0:2]
    vals = []
    for j in pre_vals:
        vals.append(j*(360 / (2*np.pi)))
    tested.append([*vals, *i[2:]])
f.close()

# Generate lists of evolving best solutions and worse solutions
deltas = []
phis = []
bad_deltas = []
bad_phis = []
best = 1e10
counter = 0
for i in tested:
    output = i[-1]

    if output < best:
        deltas.append(i[0])
        phis.append((i[1]))
        counter += 1
        best = output
        print(output)
    elif output != 1e10:
        bad_deltas.append(i[0])
        bad_phis.append((i[1]))

print(counter)
# Create contour plot and line plot
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["font.size"] = 12
plt.rcParams["figure.figsize"] = (7, 5.5)
plt.rcParams["figure.dpi"] = 150

fig = plt.figure()
contour = plt.contourf(x, y, minimum, 1000, cmap="cividis")
cbar = plt.colorbar(contour)
plt.scatter(bad_deltas, bad_phis, c="#c43e27", label="Tested worse solutions", s=10, zorder=1)
plt.plot(deltas, phis, "#a7ca17", label="Evolution of best solution", zorder=5)
plt.scatter(deltas[-1], phis[-1], c="orange", label="Best identified solution", s=50, zorder=10)
ax = plt.gca()
rect = patches.Rectangle((0, -0.02 * (360 / (2*np.pi))), 2*np.pi*(360 / (2*np.pi)), 0.04 * (360 / (2*np.pi)), alpha=0.25, color="white")
ax.add_patch(rect)
plt.legend(loc="upper right")
cbar.set_label("Minimum closest approach distance to\neither Callisto or "
               r"Ganymede centres ($\times$ 10$^{6}$ km)")
plt.xlabel(r"Starting position, $\delta$ ($\degree$)")
plt.xlim([0, 360])
plt.xticks(np.arange(0, 450, step=90))
plt.ylabel(r"Initial velocity direction, $\phi$ ($\degree$)")
# plt.title("A plot of the evolution of the best solution within the search space\n"
#           "for simulated annealing of the Jupiter capture")

plt.show()
