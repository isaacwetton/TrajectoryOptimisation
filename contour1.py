import constants
import kepler
import numpy as np
import bodies
import matplotlib as plt
from sim import Particle
from scipy.constants import G

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Create arrays of orbiter starting position and angles
deltas = np.linspace(0, 2*np.pi, 5)
phis = np.linspace(-np.pi / 4, np.pi / 4, 5)

# Initialise Jupiter object
jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

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
        orbiter = Particle.Particle(position=initpos, velocity=initvel, name="Orbiter", mu=2000.0 * G)

        # Set Orbiter-Jupiter distance for monitoring and initial time
        Jdist = initial_Jdist
        T = constants.EPOCH

        # Define variable for monitoring of closest approach to Callisto
        cal_pos = cal(T)[0:3]
        closest_approach = np.linalg.norm(cal_pos - orbiter.position)

        while Jdist <= initial_Jdist:
            orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
            orbiter.update_eulerCromer(100)
            T += 100
            Jdist = np.linalg.norm(orbiter.position - jupiter.position)
            cal_pos = cal(T)[0:3]
            cal_dist = np.linalg.norm(cal_pos - orbiter.position)
            if cal_dist < closest_approach:
                closest_approach = cal_dist

        # Record closest_approach for the delta-phi combination
        

