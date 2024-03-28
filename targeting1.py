import constants
import numpy as np
import bodies
from sim import Particle
from scipy.constants import G
from scipy.constants import g
from lamberthub import izzo2015
import pickle
import util

# Define useful constants
initial_Jdist = 1000 * constants.R_JUPITER

# Define delta & phis
delta = 4.653091591250735
phi = -0.027438378654921707

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
gan_map_lats = []
gan_map_lons = []

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
T = 59093.52549572423 * constants.DAY_IN_SECONDS

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
closest_gan = np.linalg.norm(orbiter.position - moon_obj[2].position)
closest_gan_pos = orbiter.position - moon_obj[2].position
flyby_gan_pos = moon_obj[2].position

# Thrust applied?
thrusted = False

# while Jdist <= initial_Jdist:
while Jdist == closest_jup:
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

    # Ganymede mapping points
    if 50 < np.linalg.norm(orbiter.position - moon_obj[2].position) - constants.R_GANYMEDE < 2000:
        current_pos = orbiter.position - moon_obj[2].position
        gan_map_lats.append(np.arctan(current_pos[2] / np.sqrt((current_pos[0] ** 2) + (current_pos[1] ** 2))))
        gan_map_lons.append(np.arctan2(current_pos[0], current_pos[1]))

    # If exiting range then break
    if Jdist > initial_Jdist:
        break

    # Update closest Jupiter approach
    if closest_jup > Jdist:
        closest_jup = Jdist

    # Update closest Ganymede approach
    if np.linalg.norm(orbiter.position - moon_obj[2].position) < closest_gan:
        closest_gan = np.linalg.norm(orbiter.position - moon_obj[2].position)
        closest_gan_pos = orbiter.position - moon_obj[2].position
        flyby_gan_pos = moon_obj[2].position
        T_flyby = T

# Time to reach periapsis from flyby
T_peri = T - T_flyby

# Calculate orbiter position required to map Ganymede's 20th face at altitude 2000 km
R = 2000
xf = (R + constants.R_GANYMEDE) * np.cos(30 * (2*np.pi) / 360) * np.cos(-90 * (2*np.pi) / 360) + flyby_gan_pos[0]
yf = (R + constants.R_GANYMEDE) * np.cos(30 * (2*np.pi) / 360) * np.sin(-90 * (2*np.pi) / 360) + flyby_gan_pos[1]
zf = (R + constants.R_GANYMEDE) * np.sin(30 * (2*np.pi) / 360) + flyby_gan_pos[2]
rf = np.array([xf, yf, zf], dtype=float)

# Use the Lambert solver to determine the required velocity at periapsis
ri = orbiter.position
tof = 7.15455296 * constants.DAY_IN_SECONDS - T_peri
vi, vf = izzo2015(constants.MU_JUPITER, ri, rf, tof)

# Calculation of deltaV and required propellant
delta_v_vec = vi - orbiter.velocity
delta_v = np.linalg.norm(delta_v_vec)
required_p = (orbiter.mu / G) * (1 - np.exp(-(delta_v * 1000) / (2000 * g)))

# Apply thrust by burning the required propellant
orbiter.velocity = vi
orbiter.mu -= required_p * G

# Continue evolution until around next periapsis (after 1 Ganymede period)
T_stop = T + 7.15455296 * constants.DAY_IN_SECONDS

# Track best Ganymede alt
best_gan_alt = np.linalg.norm(orbiter.position - moon_obj[2].position) - constants.R_GANYMEDE
while T < T_stop:
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

    # Ganymede mapping points
    if 50 < np.linalg.norm(orbiter.position - moon_obj[2].position) - constants.R_GANYMEDE < 2000:
        current_pos = orbiter.position - moon_obj[2].position
        gan_map_lats.append(np.arctan(current_pos[2] / np.sqrt((current_pos[0] ** 2) + (current_pos[1] ** 2))))
        gan_map_lons.append(np.arctan2(current_pos[0], current_pos[1]))

    # If exiting range then break
    if Jdist > initial_Jdist:
        break

    # Update closest Jupiter approach
    if closest_jup > Jdist:
        closest_jup = Jdist

    # Update closest Ganymede approach
    if np.linalg.norm(orbiter.position - moon_obj[2].position) < closest_gan:
        closest_gan = np.linalg.norm(orbiter.position - moon_obj[2].position)
        closest_gan_pos = orbiter.position - moon_obj[2].position
        flyby_gan_pos = moon_obj[2].position
        T_flyby = T

    # Update best Ganymede alt
    if np.linalg.norm(orbiter.position - moon_obj[2].position) - constants.R_GANYMEDE < best_gan_alt:
        best_gan_alt = np.linalg.norm(orbiter.position - moon_obj[2].position) - constants.R_GANYMEDE

# Print best Ganymede alt
print(best_gan_alt)

# Save data
f = open("data/targeting1data2.dat", "wb")
pickle.dump((orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, gan_map_lats, gan_map_lons), f, True)
f.close()
print("Done")
