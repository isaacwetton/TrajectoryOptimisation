import pickle
from matplotlib import pyplot as plt

# Load simann data
f = open("data/timeit2simann.dat", "rb")
simann_decs, simann_errors, simann_times = pickle.load(f)
f.close()

# Load monte data
f = open("data/timeit2monte.dat", "rb")
monte_sols, monte_errors, monte_times = pickle.load(f)
f.close()

# Create plot
plt.plot(monte_times, monte_errors, "k")
plt.plot(simann_times, simann_errors, "r")
plt.xlim(0.1, 1)
plt.ylim()
plt.title("A plot of runtime against temperature decrease rate\nfor Monte Carlo optimisation applied to a quadratic problem.")
plt.xlabel(r"Number of sampled solutions")
plt.ylabel("Average error")
plt.show()
