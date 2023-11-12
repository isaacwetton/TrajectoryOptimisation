import constants
import kepler
import numpy as np
import bodies
import matplotlib as plt
from sim import Particle

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Create arrays of orbiter starting position and angles
deltas = np.linspace(0, 2*np.pi, 5)
phis = np.linspace(-np.pi / 4, np.pi / 4, 5)

# Model orbiter for each delta-phi combination
for delta in deltas:

    # Calculate initial orbiter pos
    initpos = np.array([initial_Jdist * np.cos(delta), initial_Jdist * np.sin(delta), 0], dtype=float)

    for phi in phis:
        # Initialise Callisto
        cal = bodies.get_callisto()

        # Calculate initial orbiter vel
        vel_angle = delta + np.pi + phi
        initvel = np.array([3.4 * np.cos(vel_angle), 3.4 * np.sin(vel_angle), 0], dtype=float)

        # Initialise orbiter
        orbiter = Particle.Particle(position=initpos, velocity=initvel, name="Orbiter", mass=2000.0)
