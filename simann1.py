import constants
import numpy as np
import bodies
from sim import Particle
from scipy.constants import G
import util

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Define space sizes
DELTA_SIZE = 2*np.pi
PHI_SIZE = 0.2
MJD_SIZE = 62502 - 59215

for attempt in range(1):
    # Randomly define initial conditions
    delta = np.random.uniform(low=0, high=2*np.pi)
    delta0 = delta
    phi = np.random.uniform(low=-0.1, high=0.1)
    phi0 = phi
    MJD = np.random.uniform(low=59215, high=62502)
    MJD0 = MJD
    T0 = MJD * constants.DAY_IN_SECONDS

    # Set temperature for simulated annealing and variable for best result
    temp = 1
    best = (-1e10, 0, 0, 0)  # semi-major axis, delta, phi, T0

    # Initialise Jupiter
    jupiter = Particle.Particle(name="Jupiter", mu=constants.MU_JUPITER)

    # Keep evolving until temperature drops below 0
    while temp > 0:
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
        current_best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER)
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

        # Update temperature and best result
        if (best[0] < 0 and current_best > best[0]) or best[0] > current_best > 0:
            best = (current_best, delta, phi, T0)
            temp += 0.05
            delta0 = delta
            phi0 = phi
            MJD0 = MJD
        else:
            temp -= 0.005

        if temp > 1:
            temp = 1

        # Print the found semi-major axis
        # print(current_best)

        # Randomly determine new initial conditions
        delta = delta0 + np.random.uniform(low=-DELTA_SIZE * temp, high=DELTA_SIZE * temp)
        while not 0 <= delta <= 2*np.pi:
            delta = delta0 + np.random.uniform(low=-DELTA_SIZE * temp, high=DELTA_SIZE * temp)

        phi = phi0 + np.random.uniform(low=-PHI_SIZE * temp, high=PHI_SIZE * temp)
        while not -0.1 <= phi <= 0.1:
            phi = phi0 + np.random.uniform(low=-PHI_SIZE * temp, high=PHI_SIZE * temp)

        MJD = MJD0 + np.random.uniform(low=-MJD_SIZE * temp, high=MJD_SIZE * temp)
        while not 59215 <= MJD <= 62502:
            MJD = MJD0 + np.random.uniform(low=-MJD_SIZE * temp, high=MJD_SIZE * temp)
        T0 = MJD * constants.DAY_IN_SECONDS

    # Print best result
    print(best)
