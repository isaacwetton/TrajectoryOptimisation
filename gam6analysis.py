import pickle
import constants

# Load data
f = open("data/gam5data6.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, vels, Jdists = pickle.load(f)
f.close()

closest = 1000 * constants.R_JUPITER
closest_vel = 3.4

for i in range(len(Jdists)):
    if Jdists[i] < closest:
        closest = Jdists[i]
        closest_vel = vels[i]
    elif Jdists[i] > 1.1e6:
        print("Distance", Jdists[i])
        print("Velocity", vels[i])
        break


print("Periapsis distance:", closest)
print("Periapsis velocity:", closest_vel)