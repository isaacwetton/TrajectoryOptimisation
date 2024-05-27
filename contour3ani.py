import pickle
import constants
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.animation import FFMpegWriter

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

# Load test data
f = open("data/monte1test1.dat", "rb")
pre_tested = pickle.load(f)
tested = []
for i in pre_tested:
    pre_vals = i[0:2]
    vals = []
    for j in pre_vals:
        vals.append(j*(360 / (2*np.pi)))
    tested.append([*vals, i[3]])
f.close()

# Generate lists of evolving best solutions and worse solutions
# deltas = []
# phis = []
# bad_deltas = []
# bad_phis = []
# best = -1e10
# counter = 0
# for i in tested:
#     output = i[-1]
#     if output >= 1e9:
#         output = - (output - 1e9)
#
#     if best < 0 and output > best:
#         deltas.append(i[0])
#         phis.append((i[1]))
#         counter += 1
#         best = output
#         print(output)
#     elif best > output > 0:
#         deltas.append(i[0])
#         phis.append((i[1]))
#         counter += 1
#         best = output
#         print(output)
#     elif output != -1e10:
#         bad_deltas.append(i[0])
#         bad_phis.append((i[1]))
#
# print(counter)

# # Create contour plot and line plot
# fig = plt.figure()
# contour = plt.contourf(x, y, both, 1000, cmap="cividis")
# cbar = plt.colorbar(contour)
# plt.scatter(bad_deltas, bad_phis, c="red", label="Tested worse solutions", s=10)
# plt.plot(deltas, phis, "lime", label="Evolution of best solution")
# ax = plt.gca()
# rect = patches.Rectangle((0, -0.02 * (360 / (2*np.pi))), 2*np.pi*(360 / (2*np.pi)), 0.04 * (360 / (2*np.pi)), alpha=0.25, color="white")
# ax.add_patch(rect)
# plt.legend(loc="upper right")
# cbar.set_label("Sum of closest approaches to Callisto and Ganymede (km)")
# plt.xlabel(r"Starting position, $\delta$ ($\degree$)")
# plt.xlim([0, 360])
# plt.xticks(np.arange(0, 450, step=90))
# plt.ylabel(r"Initial velocity direction, $\phi$ ($\degree$)")
# plt.title("A plot of the evolution of the best solution within the search space\n"
#           "for simulated annealing of the Jupiter capture")
#
# plt.show()

# Create lists for animation
bad_phis = []
good_phis = []
bad_deltas = []
good_deltas =[]

# Animation setup
j = 0
best = 1e10

# Create figure
fig = plt.figure(figsize=(8, 6))


# Animation function
def animate(i):
    global best, j, bad_deltas, bad_phis, good_deltas, good_phis, testing_delta, testing_phi
    if j < len(tested):
        # Next tested point
        if j == len(tested) - 1:
            testing_delta = None
            testing_phi = None
        else:
            testing_delta = tested[j+1][0]
            testing_phi = tested[j+1][1]

        output = tested[j][-1]
        if output < best:
            good_deltas.append(tested[j][0])
            good_phis.append((tested[j][1]))
            best = output
            print(output)
        elif output != 1e10:
            bad_deltas.append(tested[j][0])
            bad_phis.append((tested[j][1]))
            print(tested[j])

    # Increase j
    j += 1

    # Set up plot
    fig.clf()
    ax = fig.add_subplot()
    ax.set_xlim([0, 360])
    ax.set_xlabel(r"Starting position, $\delta$ ($\degree$)")
    ax.set_ylabel(r"Initial velocity direction, $\phi$ ($\degree$)")
    # ax.set_title("A plot of the evolution of the best solution within the search space\n"
    #              "for simulated annealing of the Jupiter capture")
    ax.set_xticks(np.arange(0, 450, step=90))

    # Plot contour
    contour = ax.contourf(x, y, minimum, 1000, cmap="cividis")
    cbar = plt.colorbar(contour)
    cbar.set_label("Minimum closest approach distance to\neither Callisto or "
                   r"Ganymede centres ($\times$ 10$^{6}$ km)")

    # Plot tested solution
    if testing_delta is None:
        # Phi is 90 so does not appear on plot
        ax.scatter(0, 90, c="orange", label="Solution testing in progress", s=100)
    else:
        ax.scatter(testing_delta, testing_phi, c="orange", label="Solution testing in progress", s=100)

    # Plot bad solutions
    ax.scatter(bad_deltas, bad_phis, c="red", label="Tested worse solutions", s=10)

    # Plot best solution evolution
    ax.plot(good_deltas, good_phis, "lime", label="Evolution of best solution")

    # Plot rectangle
    rect = patches.Rectangle((0, -0.02 * (360 / (2 * np.pi))), 2 * np.pi * (360 / (2 * np.pi)),
                             0.04 * (360 / (2 * np.pi)), alpha=0.25, color="white")
    ax.add_patch(rect)

    # Add legend
    ax.legend(loc="upper right")


# Run animation
ani = FuncAnimation(fig, animate, repeat=True,
                    frames=len(tested)+1, interval=250)


# # Save animation as .gif file
# writer = PillowWriter(fps=30,
#                       metadata=dict(),
#                       bitrate=1800
#                       )
# ani.save('Plots + Animations/contour3ani.gif', writer=writer)

plt.show()
# # Save animation as .mp4 file
# writer = FFMpegWriter(fps=60)
# ani.save('Plots + Animations/contour3ani.mp4', writer=writer)
