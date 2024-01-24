from timeit import timeit
import optimise
import pickle
import numpy as np
import constants
from sim import Particle
import bodies
import util
from scipy.constants import G


def find_semimajor(delta, phi, MJD):
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
    current_best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                  constants.MU_JUPITER)
    while Jdist <= initial_Jdist and current_best < 0:
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

        # Determine whether semi-major axis is better
        if current_best < util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                         constants.MU_JUPITER):
            current_best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                          constants.MU_JUPITER)

        # Update moon parameters
        for i in range(4):
            moon_states[i] = moons[i](T)
            moon_obj[i].position = np.array(moon_states[i][0:3], dtype=float)

    # Continue evolution if capture is accomplished
    if current_best > 0:
        print("capture")
        for x in range(10000):
            # Calculate acceleration
            orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
            for i in range(4):
                orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[i])

            # Evolve with timestep depending on Jupiter distance
            if Jdist > 30 * constants.R_JUPITER:
                deltaT = 500
            else:
                deltaT = 2

            T += deltaT
            orbiter.update_eulerCromer(deltaT)
            Jdist = np.linalg.norm(orbiter.position - jupiter.position)

            # Determine whether semi-major axis is better
            if current_best < util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                             constants.MU_JUPITER):
                current_best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                              constants.MU_JUPITER)

            # Update moon parameters
            for i in range(4):
                moon_states[i] = moons[i](T)
                moon_obj[i].position = np.array(moon_states[i][0:3], dtype=float)

    return util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER)


tests = 1
setup = """
import optimise
import numpy as np
import constants
from sim import Particle
import bodies
import util
from scipy.constants import G

def find_semimajor(delta, phi, MJD):
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
    current_best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                  constants.MU_JUPITER)
    while Jdist <= initial_Jdist and current_best < 0:
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

        # Determine whether semi-major axis is better
        if current_best < util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                         constants.MU_JUPITER):
            current_best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                          constants.MU_JUPITER)

        # Update moon parameters
        for i in range(4):
            moon_states[i] = moons[i](T)
            moon_obj[i].position = np.array(moon_states[i][0:3], dtype=float)

    # Continue evolution if capture is accomplished
    if current_best > 0:
        print("capture")
        for x in range(10000):
            # Calculate acceleration
            orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
            for i in range(4):
                orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[i])

            # Evolve with timestep depending on Jupiter distance
            if Jdist > 30 * constants.R_JUPITER:
                deltaT = 500
            else:
                deltaT = 2

            T += deltaT
            orbiter.update_eulerCromer(deltaT)
            Jdist = np.linalg.norm(orbiter.position - jupiter.position)

            # Determine whether semi-major axis is better
            if current_best < util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                             constants.MU_JUPITER):
                current_best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                              constants.MU_JUPITER)

            # Update moon parameters
            for i in range(4):
                moon_states[i] = moons[i](T)
                moon_obj[i].position = np.array(moon_states[i][0:3], dtype=float)

    return util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER)
"""

simann_decs = [0.1, 0.075, 0.05, 0.025, 0.02, 0.01]
simann_times = []
simann_errors = []

for i in range(len(simann_decs)):
    t_simann = timeit("result, vals = optimise.simann(find_semimajor, 0.1, " + str(simann_decs[i]) + ", 0.0, 1.0, (0, 2*np.pi), (-0.005, 0.005), (59215, 59232))",
                      setup=setup, number=tests)
    simann_times.append(t_simann / tests)
    errors = 0
    for j in range(tests):
        result, vals = optimise.simann(find_semimajor, 0.1, simann_decs[i], 0.0, 1.0, (0, 2*np.pi), (-0.005, 0.005), (59215, 59232))
        errors += abs(result)
    simann_errors.append(errors / tests)

# Save simann data
f = open("data/timeit3simann.dat", "wb")
pickle.dump((simann_decs, simann_errors, simann_times), f, True)
f.close()
