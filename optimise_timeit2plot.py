import pickle
from matplotlib import pyplot as plt

# Load simann data
f = open("data/timeitFsimann.dat", "rb")
simann_decs, simann_errors, simann_times = pickle.load(f)
f.close()

# Load monte data
f = open("data/timeitFmonte.dat", "rb")
monte_sols, monte_errors, monte_times = pickle.load(f)
f.close()

# Load monte2 data
f = open("data/timeit2monte.dat", "rb")
monte2_sols, monte2_errors, monte2_times = pickle.load(f)
f.close()

# Create plot
plt.rcParams["font.family"] = "Kepler", "Kepler Std", "serif"
plt.rcParams["font.size"] = 11
plt.rcParams["figure.figsize"] = (7, 5.5)
plt.rcParams["figure.dpi"] = 150


# plt.plot(monte_times, monte_errors, "#342f29")
# plt.plot(simann_times, simann_errors, "#c43e27")
plt.plot(monte2_times[10:30], monte2_errors[10:30], "#39667b")
plt.plot(simann_times[65:90], simann_errors[65:90], "#c43e27")
plt.plot(monte_times[10:31], monte_errors[10:31], "#342f29")
# plt.plot(monte_sols, monte_times, "k")
# plt.title("A plot of average error against optimisation runtime for Monte Carlo and\nsimulated annealing optimisation methods applied to a quadratic problem.")
plt.xlabel(r"Optimisation runtime (s)", fontsize=15)
plt.ylabel("Average error", fontsize=15)
plt.legend(["Single-stage Monte Carlo", "Simulated Annealing", "Dual-stage Monte Carlo"], fontsize=15)
plt.show()
