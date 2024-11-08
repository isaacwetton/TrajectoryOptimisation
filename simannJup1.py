import optimise
import numpy as np
import constants
from sim import Particle
import bodies
import util
from scipy.constants import G
import pickle


def find_semimajor(delta, phi, MJD):
    if -0.02 < phi < 0.02:
        print("Abs(phi) too small")
        return -1e10

    T0 = MJD * constants.DAY_IN_SECONDS
    initial_Jdist = 1000 * constants.R_JUPITER

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

        # Return poor result if collision with Jupiter
        if np.linalg.norm(orbiter.position - jupiter.position) < 2 * constants.R_JUPITER:
            print("Jupiter collision")
            return -1e10

        # Return poor result if collision with moon
        if np.linalg.norm(orbiter.position - moon_obj[0].position) < 50 + moon_radii[0]:
            print("Io collision")
            return -1e10
        elif np.linalg.norm(orbiter.position - moon_obj[1].position) < 50 + moon_radii[1]:
            print("Europa collision")
            return -1e10
        elif np.linalg.norm(orbiter.position - moon_obj[2].position) < 50 + moon_radii[2]:
            print("Ganymede collision")
            return -1e10
        elif np.linalg.norm(orbiter.position - moon_obj[3].position) < 50 + moon_radii[3]:
            print("Callisto collision")
            return -1e10

        # Update closest Jupiter approach and break if leaving 30 Jupiter radii
        if closest_jup > Jdist:
            closest_jup = Jdist
        elif Jdist > closest_jup + 25 * constants.R_JUPITER:
            break

    # Return positive semi-major axis or modified negative semi-major axis
    # If semi-major axis is >1e9, it is likely negative: subtract 1e9 and invert sign to retrieve
    semimajor = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER)
    print(semimajor)
    if semimajor > 0:
        return semimajor
    else:
        return 1e9 + abs(semimajor)


result, vals, tested = optimise.simann(find_semimajor, 0.1, 0.0025, 1880000.0, 1.0, (4.0, 2*np.pi), (-0.1, 0.1), (59228.5, 59229.5), track_evolution=True)
print(vals)
print(result)

# Save data
f = open("data/simannJup1tested1.dat", "wb")
pickle.dump(tested, f, True)
f.close()
