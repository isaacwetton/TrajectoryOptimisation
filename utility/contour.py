import constants
import numpy as np
import bodies
import matplotlib.pyplot as plt

T = 2000.0 * constants.R_JUPITER / 3.4
print(T)
times0 = np.linspace(0, T, 1000)
times = np.linspace(0, T, 1000) + constants.EPOCH_MJD0 * constants.DAY_IN_SECONDS
cal = bodies.get_callisto()
state = cal(times)

dist = []
for i, t in zip(state, times0):
    dist.append(
        np.sqrt((30.0 * constants.R_JUPITER - i[0]) ** 2 + ((1000 * constants.R_JUPITER - t * 3.4) - i[1]) ** 2))

plt.plot(times, dist, '-', c="tab:purple")
plt.show()
