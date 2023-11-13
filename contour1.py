import constants
import numpy as np
import bodies
from matplotlib import pyplot as plt
from matplotlib import ticker as tck
from sim import Particle
from scipy.constants import G

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Create arrays of orbiter starting position and angles
s1, s2 = 10, 10
deltas = np.linspace(0, 2*np.pi, s1)
phis = np.linspace(-np.pi / 4, np.pi / 4, s2)
x, y = np.meshgrid(deltas, phis)
z = np.zeros((s1, s2))

# Define variable for monitoring of global best solution
best = np.array([0, 0, initial_Jdist], dtype=float)

# Initialise Jupiter object
jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

# Model orbiter for each delta-phi combination
for i in range(0, len(deltas)):
    delta = deltas[i]
    # Calculate initial orbiter pos
    initpos = np.array([initial_Jdist * np.cos(delta), initial_Jdist * np.sin(delta), 0], dtype=float)

    for j in range(0, len(phis)):
        phi = phis[j]
        # Initialise Callisto
        cal = bodies.get_callisto()

        # Calculate initial orbiter vel
        vel_angle = delta + np.pi + phi
        initvel = np.array([3.4 * np.cos(vel_angle), 3.4 * np.sin(vel_angle), 0], dtype=float)

        # Initialise orbiter
        orbiter = Particle.Particle(position=initpos, velocity=initvel, name="Orbiter", mu=2000.0 * G)

        # Set Orbiter-Jupiter distance for monitoring and initial time
        Jdist = initial_Jdist
        T = constants.EPOCH

        # Define variable for monitoring of closest approach to Callisto
        cal_pos = cal(T)[0:3]
        closest_approach = np.linalg.norm(cal_pos - orbiter.position)

        while Jdist <= initial_Jdist:
            orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
            deltaT = 200
            orbiter.update_eulerCromer(deltaT)
            T += deltaT
            Jdist = np.linalg.norm(orbiter.position - jupiter.position)
            cal_pos = cal(T)[0:3]
            cal_dist = np.linalg.norm(cal_pos - orbiter.position)
            if cal_dist < closest_approach:
                closest_approach = cal_dist
                if cal_dist < best[2]:
                    best = np.array([delta, phi, cal_dist], dtype=float)

        # Record closest_approach for the delta-phi combination
        z[j][i] = closest_approach

# Create contour plot
fig = plt.figure()
contour = plt.contourf(x, y, z, 500)
cbar = plt.colorbar(contour)
cbar.set_label("Closest Approach to Callisto (km)")
plt.xlabel(r"$\delta$ (rad)")
plt.ylabel(r"$\phi$ (rad)")
plt.title("Contour plot of Closest Approach to Callisto (km) as a Function of delta and phi")
# plt.ylim([-np.pi / 4, np.pi / 4])
# plt.xlim([0, 2*np.pi])

# ax.xaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
# ax.xaxis.set_major_locator(tck.MultipleLocator(base=1/2))
# ax.yaxis.set_major_formatter(tck.FormatStrFormatter('%g $\pi$'))
# ax.yaxis.set_major_locator(tck.MultipleLocator(base=1/4))
# plt.style.use("ggplot")

plt.show()


