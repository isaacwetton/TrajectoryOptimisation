import constants
import numpy as np
import bodies
from sim import Particle
from scipy.constants import G
from matplotlib import pyplot as plt

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Initialise Jupiter object
jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

# Model orbiter for each delta-phi combination
phi = 0.0833
delta = 0.778

# Initialise Callisto
cal = bodies.get_callisto()

# Calculate initial orbiter pos
initpos = np.array([initial_Jdist * np.cos(delta), initial_Jdist * np.sin(delta), 0], dtype=float)

# Calculate initial orbiter vel
vel_angle = delta + np.pi + phi
initvel = np.array([3.4 * np.cos(vel_angle), 3.4 * np.sin(vel_angle), 0], dtype=float)

# Initialise orbiter
orbiter = Particle.Particle(position=initpos, velocity=initvel, name="Orbiter", mu=2000.0 * G)

# Initial time
T = constants.EPOCH

# Define variable for monitoring of closest approach to Callisto
cal_pos = cal(T)[0:3]
closest_approach = np.linalg.norm(cal_pos - orbiter.position)

times = []
pos = []

Jdist = 1000 * constants.R_JUPITER
while Jdist <= initial_Jdist:
    orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
    deltaT = 200
    orbiter.update_eulerCromer(deltaT)
    T += deltaT
    Jdist = np.linalg.norm(orbiter.position - jupiter.position)
    cal_state = cal(T)
    cal_dist = np.linalg.norm(cal_pos - orbiter.position)


    # Coordinates in callisto-centred rotating frame
    x = cal_state[3:6] / np.linalg.norm(cal_state[3:6])
    y = - (cal_state[0:3] / np.linalg.norm(cal_state[0:3]))
    z = np.cross(x, y)
    orb_pos = orbiter.position[:3] - cal_state[0:3]
    if Jdist < 1000 * constants.R_JUPITER:
        pos.append(np.array([orb_pos.dot(x), orb_pos.dot(y), orb_pos.dot(z)]))
        times.append(T)

# Set starting time to zero
for i in range(0, len(times)):
    times[i] -= constants.EPOCH

# Create plot
pos = np.array(pos)
fig = plt.figure()
# plt.semilogy(times, accs_jup, "r")
# plt.semilogy(times, accs_cal, "k")
plt.plot(pos[:,0], pos[:,1])
plt.xlabel(r"x (km)")
plt.ylabel(r"y (km)")
# plt.xlim(0, 3.5e7)
# plt.legend(["Jupiter", "Callisto"])
plt.title(r"Orbiter trajectory in the Callisto-centred rotating coordinate frame for $\delta = 0.778$, $\phi = 0.0833$")
plt.show()
