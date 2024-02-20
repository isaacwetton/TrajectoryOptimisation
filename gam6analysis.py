import pickle
import constants

# Load data
f = open("data/gam6data1.dat", "rb")
Jdists, vels = pickle.load(f)
f.close()

closest = 1000 * constants.R_JUPITER
closest_vel = 3.4
for i in range(len(Jdists)):
    if Jdists[i] < closest:
        closest = Jdists[i]
        closest_vel = vels[i]

print(closest)
print(closest_vel)