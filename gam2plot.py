import pickle
from matplotlib import pyplot as plt

# Load data
f = open("data/gam2data8.dat", "rb")
phis, bests, finals = pickle.load(f)
f.close()

# Create plot
plt.plot(phis, bests)
plt.title(r"A plot of best semi-major axis of Jupiter orbit against $\phi$")
plt.xlabel(r"$\phi$ (rad)")
plt.ylabel("Semi-major axis")
plt.show()
