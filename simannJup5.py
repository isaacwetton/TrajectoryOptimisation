import optimise
import numpy as np
import constants
from sim import Particle
import bodies
import util
from scipy.constants import G, g
from scipy.interpolate import RegularGridInterpolator
import pickle

# Load data
f = open("data/contour3data4.dat", "rb")
(x, y, closest_cal, closest_gan) = pickle.load(f)
both = closest_cal + closest_gan
both2 = np.matrix.transpose(both)  # Required matrix transpose???
f.close()

# Create interpolator
s1, s2 = 25, 25
deltas = np.linspace(0, 2*np.pi, s1)
phis = np.linspace(-0.2, 0.2, s2, endpoint=True)
interp = RegularGridInterpolator((deltas, phis), both2)


def find_semimajor(delta, phi, MJD):
    if -0.02 < phi < 0.02:
        print("Abs(phi) too small")
        return 1e10

    if interp((delta, phi)) > 0.3e7 and np.random.uniform(low=0.0, high=1.0) < 0.75:
        print("Poor interpolation result")
        return 1e10

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
    closest_vel = np.linalg.norm(orbiter.velocity)
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
            return 1e10

        # Return poor result if collision with moon
        if np.linalg.norm(orbiter.position - moon_obj[0].position) < 50 + moon_radii[0]:
            print("Io collision")
            return 1e10
        elif np.linalg.norm(orbiter.position - moon_obj[1].position) < 50 + moon_radii[1]:
            print("Europa collision")
            return 1e10
        elif np.linalg.norm(orbiter.position - moon_obj[2].position) < 50 + moon_radii[2]:
            print("Ganymede collision")
            return 1e10
        elif np.linalg.norm(orbiter.position - moon_obj[3].position) < 50 + moon_radii[3]:
            print("Callisto collision")
            return 1e10

        # Update closest Jupiter approach and break if leaving 5 Jupiter radii
        if closest_jup > Jdist:
            closest_jup = Jdist
            closest_vel = np.linalg.norm(orbiter.velocity)
        elif Jdist > closest_jup:
            break
        elif 5 * constants.R_JUPITER > util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER) > 0:
            break

    # Return positive semi-major axis or modified negative semi-major axis
    # If semi-major axis is >1e9, it is likely negative: subtract 1e9 and invert sign to retrieve
    semimajor = util.semimajor(np.linalg.norm(orbiter.position), np.linalg.norm(orbiter.velocity), constants.MU_JUPITER)
    apo = 1950000
    target_a = (apo + closest_jup) / 2
    target_v = np.sqrt(constants.MU_JUPITER * ((2 / closest_jup) - (1 / target_a)))
    delta_v = abs(closest_vel - target_v)
    required_p = 2000 * (1 - np.exp(-(delta_v * 1000) / (2000 * g)))
    print(required_p)
    return required_p


result, vals, tested = optimise.simann(find_semimajor, 0.05, 0.001, 0, 1.0, (1.0, 2.0), (0.05, 0.1), (59226.67, 59227.17), track_evolution=True)
print(vals)
print(result)

# Save data
f = open("data/simannJup5tested1.dat", "wb")
pickle.dump(tested, f, True)
f.close()
