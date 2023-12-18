import constants
import numpy as np
import bodies
from sim import Particle
from scipy.constants import G
import pickle
import util

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Define delta & phis
delta = 0.778
phi = 0.0831

# Define tuple to store closest approach time & distance
closest = (constants.EPOCH, 1000 * constants.R_JUPITER)

# Initialise Jupiter
jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

# Calculate initial orbiter pos
initpos = np.array([initial_Jdist * np.cos(delta), initial_Jdist * np.sin(delta), 0], dtype=float)

# Calculate initial orbiter vel
vel_angle = delta + np.pi + phi
initvel = np.array([3.4 * np.cos(vel_angle), 3.4 * np.sin(vel_angle), 0], dtype=float)

# Initialise orbiter
orbiter = Particle.Particle(position=initpos, velocity=initvel, name="Orbiter", mu=2000.0 * G)

# Initial time
T = constants.EPOCH

# Initialise Galilean Moon Objects
moons = [bodies.get_io(), bodies.get_europa(), bodies.get_ganymede(), bodies.get_callisto()]

# Find initial moon states
moon_states = [None] * 4
for i in range(4):
    moon_states[i] = moons[i](T)

moon_obj = [Particle.Particle(name="Io", mu=constants.MU_IO, position=np.array(moon_states[0][0:3], dtype=float)),
            Particle.Particle(name="Europa", mu=constants.MU_EUROPA,
                              position=np.array(moon_states[1][0:3], dtype=float)),
            Particle.Particle(name="Ganymede", mu=constants.MU_GANYMEDE,
                              position=np.array(moon_states[2][0:3], dtype=float)),
            Particle.Particle(name="Callisto", mu=constants.MU_CALLISTO,
                              position=np.array(moon_states[3][0:3], dtype=float))]

# Set initial Jupiter distance
Jdist = initial_Jdist

# Evolve
while Jdist <= initial_Jdist:
    # Calculate acceleration
    orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
    for i in range(4):
        orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[i])

    # Evolve with timestep depending on Jupiter distance
    if Jdist > 50 * constants.R_JUPITER:
        deltaT = 200
    else:
        deltaT = 2

    T += deltaT
    orbiter.update_eulerCromer(deltaT)
    Jdist = np.linalg.norm(orbiter.position - jupiter.position)

    # Update moon parameters
    for i in range(4):
        moon_states[i] = moons[i](T)
        moon_obj[i].position = np.array(moon_states[i][0:3], dtype=float)

    # Determine whether closest approach is better
    if np.linalg.norm(orbiter.position - moon_obj[3].position) < closest[1]:
        closest = (T, np.linalg.norm(orbiter.position - moon_obj[3].position))

print(closest)
