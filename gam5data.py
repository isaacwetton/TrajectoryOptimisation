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
delta = 4.795672919096887
phi = -0.046174926549546455

# Define lists to store results
orbpos = []
orbvel = []
calpos = []
ganpos = []
iopos = []
eurpos = []
semimajors = []
times = []

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
T = 59229.35162893285 * constants.DAY_IN_SECONDS

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

# Set initial Jupiter distance
Jdist = initial_Jdist

# Evolve and record positions
best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER)
while Jdist <= initial_Jdist and best < 0:
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

    # Determine whether semi-major axis is better
    if best < util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER):
        best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER)

    # Append results to lists
    orbpos.append(orbiter.position)
    orbvel.append(orbiter.velocity)
    calpos.append(moon_obj[3].position)
    ganpos.append(moon_obj[2].position)
    iopos.append(moon_obj[0].position)
    eurpos.append(moon_obj[1].position)
    semimajors.append(util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER))
    times.append(T)

# Continue evolution
for i in range(1000000):
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

    # Determine whether semi-major axis is better
    if best < util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                             constants.MU_JUPITER):
        best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                              constants.MU_JUPITER)

    # Append results to lists
    orbpos.append(orbiter.position)
    orbvel.append(orbiter.velocity)
    calpos.append(moon_obj[3].position)
    ganpos.append(moon_obj[2].position)
    iopos.append(moon_obj[0].position)
    eurpos.append(moon_obj[1].position)
    semimajors.append(util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                     constants.MU_JUPITER))
    times.append(T)

# Print final semi-major axis
print(util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                         constants.MU_JUPITER))
print(best)

# Save data
f = open("data/gam5data4.dat", "wb")
pickle.dump((orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times), f, True)
f.close()
print("Done")
