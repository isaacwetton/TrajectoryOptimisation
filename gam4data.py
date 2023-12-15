# This script will find the closest approach to Callisto then move the spacecraft towards Callisto to a 50km altitude.
# It will then evolve backwards to find an ideal starting point.

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
phis = np.linspace(0.0637, 0.0638, 100)

# Define lists to store results
bests = []
finals = []

# Initialise Jupiter
jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

# Tracking of closest Callisto approach (phi, dist)
closest = (0, initial_Jdist)

# Evolve for each phi

for phi in phis:
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

    # Evolve and record least negative semi-major axis
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

        # Determine if closer approach has been made
        if np.linalg.norm(orbiter.position - moon_obj[])


    # Append best semi-major axis to semi-majors
    bests.append(best)
    finals.append(util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER))
    print(best)

# Save data
f = open("data/gam2data6.dat", "wb")
pickle.dump((phis, bests, finals), f, True)
f.close()
