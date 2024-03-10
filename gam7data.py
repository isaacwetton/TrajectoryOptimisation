import constants
import numpy as np
import bodies
from sim import Particle
from scipy.constants import G
from scipy.constants import g
import pickle
import util

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Define delta & phis
delta = 4.349334252624266
phi = -0.02484535847389848

# Define lists to store results
orbpos = []
orbvel = []
calpos = []
ganpos = []
iopos = []
eurpos = []
semimajors = []
times = []
vels = []
Jdists = []

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
T = 59227.31006384439 * constants.DAY_IN_SECONDS

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
closest_jup = Jdist

# Thrust applied?
thrusted = False

# while Jdist <= initial_Jdist:
for i in range(3000000):
    # Calculate acceleration
    orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
    orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[0])
    orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[1])
    orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[2])
    orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[3])

    # Evolve with timestep depending on Jupiter distance
    if Jdist > 50 * constants.R_JUPITER:
        deltaT = 50
    elif thrusted and Jdist < 10 * constants.R_JUPITER:
        deltaT = 0.25
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

    # Apply thrust at periapsis
    if abs(Jdist - 143421) < 1.0 and not thrusted:
        print(np.linalg.norm(orbiter.velocity))
        orbiter.mu -= 153.1 * G
        delta_v = (2000 * g * np.log(2000 / (2000 - 153.1))) / 1000
        unitvec_vel = orbiter.velocity / np.linalg.norm(orbiter.velocity)
        delta_v_vec = delta_v * -unitvec_vel
        orbiter.velocity += delta_v_vec
        print(np.linalg.norm(delta_v_vec))
        print(np.linalg.norm(orbiter.velocity))
        thrusted = True

    # Output message if Jupiter collision occurs
    if Jdist < 2 * constants.R_JUPITER:
        print("Invalid solution: Jupiter collision")

    # Append results to lists
    orbpos.append(orbiter.position)
    orbvel.append(orbiter.velocity)
    calpos.append(moon_obj[3].position)
    ganpos.append(moon_obj[2].position)
    iopos.append(moon_obj[0].position)
    eurpos.append(moon_obj[1].position)
    semimajors.append(util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER))
    times.append(T)
    vels.append(np.linalg.norm(orbiter.velocity))
    Jdists.append(np.linalg.norm(orbiter.position))

    # If exiting range then break
    if Jdist > initial_Jdist:
        break

    # Update closest Jupiter approach
    if closest_jup > Jdist:
        closest_jup = Jdist


# # Continue evolution
# for i in range(1000000):
#     # Calculate acceleration
#     orbiter.acceleration = orbiter.updateGravitationalAcceleration(jupiter)
#     orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[0])
#     orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[1])
#     orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[2])
#     orbiter.acceleration += orbiter.updateGravitationalAcceleration(moon_obj[3])
#
#     # Evolve with timestep depending on Jupiter distance
#     if Jdist > 50 * constants.R_JUPITER:
#         deltaT = 50
#     else:
#         deltaT = 1
#
#     T += deltaT
#     orbiter.update_eulerCromer(deltaT)
#     Jdist = np.linalg.norm(orbiter.position - jupiter.position)
#
#     # Update moon parameters
#     moon_states = [moons[0](T), moons[1](T), moons[2](T), moons[3](T)]
#     moon_obj[0].position = np.array(moon_states[0][0:3], dtype=float)
#     moon_obj[1].position = np.array(moon_states[1][0:3], dtype=float)
#     moon_obj[2].position = np.array(moon_states[2][0:3], dtype=float)
#     moon_obj[3].position = np.array(moon_states[3][0:3], dtype=float)
#
#     # Determine whether semi-major axis is better
#     if best < util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
#                              constants.MU_JUPITER):
#         best = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
#                               constants.MU_JUPITER)
#
#     # Append results to lists
#     orbpos.append(orbiter.position)
#     orbvel.append(orbiter.velocity)
#     calpos.append(moon_obj[3].position)
#     ganpos.append(moon_obj[2].position)
#     iopos.append(moon_obj[0].position)
#     eurpos.append(moon_obj[1].position)
#     semimajors.append(util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
#                                      constants.MU_JUPITER))
#     times.append(T)

# Print final semi-major axis
print(util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity),
                                         constants.MU_JUPITER))

# Print closest_jup
print(closest_jup)

# Save data
f = open("data/gam7data2.dat", "wb")
pickle.dump((orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, vels, Jdists), f, True)
f.close()
print("Done")
