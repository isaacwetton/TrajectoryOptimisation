import constants
import numpy as np
import bodies
import pickle
from sim import Particle
from scipy.constants import G
from matplotlib import pyplot as plt

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Initialise Jupiter object
jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

# Model orbiter for each delta-phi combination
phi = 0.025
delta = 0.5

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
accs_jup = []
accs_cal = []
pos = []

Jdist = 1000 * constants.R_JUPITER
while Jdist <= initial_Jdist:
    orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
    deltaT = 200
    orbiter.update_eulerCromer(deltaT)
    T += deltaT
    Jdist = np.linalg.norm(orbiter.position - jupiter.position)
    cal_pos = cal(T)[0:3]
    cal_dist = np.linalg.norm(cal_pos - orbiter.position)
    acc_cal = constants.MU_CALLISTO / (cal_dist ** 2)
    times.append(T)
    accs_cal.append(acc_cal)
    accs_jup.append(np.linalg.norm(orbiter.acceleration))
    pos.append(orbiter.position[:2])

pos = np.array(pos)
fig = plt.figure()
plt.semilogy(times, accs_jup, "k")
plt.semilogy(times, accs_cal, "r")
# plt.plot(pos[:,0], pos[:,1])
plt.show()



