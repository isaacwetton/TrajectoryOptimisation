import numpy as np
import constants
from sim import Particle
import bodies
import util
from scipy.constants import G
import pickle

# Create arrays of orbiter starting position and angles
s1, s2 = 25, 25
deltas = np.linspace(0, 2*np.pi, s1)
phis = np.linspace(-0.2, 0.2, s2, endpoint=True)
x, y = np.meshgrid(deltas, phis)
closest_cal = np.zeros((s2, s1))
closest_gan = np.zeros((s2, s1))
solutions = s1 * s2
counter = 0

# Define constants
T0 = 59222.05 * constants.DAY_IN_SECONDS
initial_Jdist = 1000 * constants.R_JUPITER

# Initialise Jupiter
jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

for i in range(0, len(deltas)):
    delta = deltas[i]
    # Calculate initial orbiter pos
    initpos = np.array([initial_Jdist * np.cos(delta), initial_Jdist * np.sin(delta), 0], dtype=float)

    for j in range(0, len(phis)):
        phi = phis[j]
        # Calculate initial orbiter vel
        vel_angle = delta + np.pi + phi
        initvel = np.array([3.4 * np.cos(vel_angle), 3.4 * np.sin(vel_angle), 0], dtype=float)

        # Initialise orbiter
        orbiter = Particle.Particle(position=initpos, velocity=initvel, name="Orbiter", mu=2000.0 * G)

        # Initial time
        T = T0

        # Initialise Galilean Moon Objects
        moons = [bodies.get_io(), bodies.get_europa(), bodies.get_ganymede(), bodies.get_callisto()]

        # Find initial moon states
        moon_states = [moons[0](T), moons[1](T), moons[2](T), moons[3](T)]

        moon_obj = [Particle.Particle(name="Io", mu=constants.MU_IO, position=np.array(moon_states[0][0:3], dtype=float)),
                    Particle.Particle(name="Europa", mu=constants.MU_EUROPA,
                                      position=np.array(moon_states[1][0:3], dtype=float)),
                    Particle.Particle(name="Ganymede", mu=constants.MU_GANYMEDE,
                                      position=np.array(moon_states[2][0:3], dtype=float)),
                    Particle.Particle(name="Callisto", mu=constants.MU_CALLISTO,
                                      position=np.array(moon_states[3][0:3], dtype=float))]

        # Define moon radii
        moon_radii = [constants.R_IO, constants.R_EUROPA, constants.R_GANYMEDE, constants.R_CALLISTO]

        # Set initial Jupiter distance
        Jdist = initial_Jdist

        # Values for tracking
        closest_cal_track = np.linalg.norm(orbiter.position - moon_obj[3].position)
        closest_gan_track = np.linalg.norm(orbiter.position - moon_obj[2].position)

        # Evolve
        closest_jup = initial_Jdist
        while Jdist <= initial_Jdist:
            # Calculate acceleration
            orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
            orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[0])
            orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[1])
            orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[2])
            orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[3])

            # Evolve with timestep depending on Jupiter distance
            if Jdist > 50 * constants.R_JUPITER:
                deltaT = 50
            else:
                deltaT = 1

            T += deltaT
            orbiter.update_eulerCromer(deltaT)
            Jdist = np.linalg.norm(orbiter.position - jupiter.position)

            # Update moon parameters
            moon_states = [moons[0](T), moons[1](T), moons[2](T), moons[3](T)]
            moon_obj[0].position = np.array(moon_states[0][0:3], dtype=float)
            moon_obj[1].position = np.array(moon_states[1][0:3], dtype=float)
            moon_obj[2].position = np.array(moon_states[2][0:3], dtype=float)
            moon_obj[3].position = np.array(moon_states[3][0:3], dtype=float)

            # Update closest moon approach values
            if closest_cal_track > np.linalg.norm(orbiter.position - moon_obj[3].position):
                closest_cal_track = np.linalg.norm(orbiter.position - moon_obj[3].position)
            if closest_gan_track > np.linalg.norm(orbiter.position - moon_obj[2].position):
                closest_gan_track = np.linalg.norm(orbiter.position - moon_obj[2].position)

            # Update closest Jupiter approach and break after periapsis
            if closest_jup > Jdist:
                closest_jup = Jdist
            elif Jdist > closest_jup:
                break

        # Fill in value grids for contour
        closest_cal[j][i] = closest_cal_track
        closest_gan[j][i] = closest_gan_track
        counter += 1
        print("Completed test of solution " + str(counter) + " of " + str(solutions))

# Save data
f = open("data/contour3data5.dat", "wb")
pickle.dump((x, y, closest_cal, closest_gan), f, True)
f.close()
