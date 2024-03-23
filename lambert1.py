from lamberthub import izzo2015
import constants
import numpy as np

ri = np.array([24299.61728233, 149148.49499682, -592.11319199], dtype=float)
rf = np.array([6.07448341e+05, -8.79573365e+05, -2.01639866e+02], dtype=float)
tof = 6.51733 * constants.DAY_IN_SECONDS

vi, vf = izzo2015(constants.MU_JUPITER, ri, rf, tof)
print(vi)