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
acc_cal = 0

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

# Evolve until entering Callisto's SOI
orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
while Jdist <= initial_Jdist:
    deltaT = 200
    orbiter.update_eulerCromer(deltaT)
    T += deltaT
    orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
    Jdist = np.linalg.norm(orbiter.position - jupiter.position)
    cal_pos = cal(T)[0:3]
    cal_dist = np.linalg.norm(cal_pos - orbiter.position)
    acc_cal = constants.MU_CALLISTO / (cal_dist ** 2)
    times.append(T)
    accs_cal.append(acc_cal)
    accs_jup.append(np.linalg.norm(orbiter.acceleration))
    pos.append(orbiter.position[:2])
    # BREAK IF ENTERING CALLISTO SOI & OUTPUT R
    if acc_cal > np.linalg.norm(orbiter.acceleration):
        print("r_c = " + str(cal_dist))
        # Calculate Callisto-centric velocity
        v_c = orbiter.velocity - cal(T)[3:6]
        print(np.linalg.norm(v_c))
        break

# Evolve until exiting Callisto's SOI
callisto = Particle.Particle(name="Callisto", mu=constants.MU_CALLISTO)
cal_state = cal(T)
callisto.position = cal_state[0:3]
callisto.velocity = cal_state[3:6]
acc_jup = np.linalg.norm(orbiter.acceleration)
orbiter.acceleration = orbiter.updateGravitationalAcceleration(callisto)
while acc_cal > acc_jup:
    deltaT = 20
    orbiter.update_eulerCromer(deltaT)
    T += deltaT
    cal_state = cal(T)
    callisto.position = cal_state[0:3]
    callisto.velocity = cal_state[3:6]
    orbiter.acceleration = orbiter.updateGravitationalAcceleration(callisto)
    acc_cal = np.linalg.norm(orbiter.acceleration)
    acc_jup = np.linalg.norm(orbiter.updateGravitationalAcceleration(jupiter))
    times.append(T)
    pos.append(orbiter.position[:2])

# Evolve further
orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
for i in range(0, 100000):
    deltaT = 200
    orbiter.update_eulerCromer(deltaT)
    T += deltaT
    orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
    Jdist = np.linalg.norm(orbiter.position - jupiter.position)
    times.append(T)
    pos.append(orbiter.position[:2])
    if Jdist > initial_Jdist:
        break

# Set starting time to zero
for i in range(0, len(times)):
    times[i] -= constants.EPOCH

# Create plot
pos = np.array(pos)
fig = plt.figure()
plt.plot(pos[:,0], pos[:,1])
plt.xlabel(r"x (km)")
plt.ylabel(r"y (km)")
plt.show()
