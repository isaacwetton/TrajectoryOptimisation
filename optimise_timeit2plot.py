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
plt.plot(monte_times[15:35], monte_errors[15:35], "k")
plt.plot(simann_times[60:90], simann_errors[60:90], "r")
# plt.plot(monte_sols, monte_times, "k")
plt.title("A plot of average error against optimisation runtime for Monte Carlo and\nsimulated annealing optimisation methods applied to a quadratic problem.")
plt.xlabel(r"Optimisation runtime (s)")
plt.ylabel("Average error")
plt.legend(["Single-stage Monte Carlo", "Simulated Annealing"])
plt.show()
