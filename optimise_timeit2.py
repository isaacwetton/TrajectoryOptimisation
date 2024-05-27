from timeit import timeit
import optimise
import pickle
import numpy as np

def quadratic(x):
    return 4 * x * x + 4 * x + 1


tests = 10
setup = """
import optimise

def quadratic(x):
    return 4 * x * x + 4 * x + 1
"""

# simann_decs = ["0.1", "0.05", "0.01", "0.005", "0.001", "0.0005", "0.0001", "0.00005", "0.00001", "0.000005"]
simann_decs = np.exp(np.linspace(-12, -3, 100))
simann_times = []
simann_errors = []

for i in range(len(simann_decs)):
    t_simann = timeit("result, vals = optimise.simann(quadratic, 0.1, " + str(simann_decs[i]) + ", 0.0, 1.0, (-5.0, 5.0))",
                      setup=setup, number=tests)
    simann_times.append(t_simann / tests)
    errors = 0
    for j in range(tests):
        result, vals = optimise.simann(quadratic, 0.1, simann_decs[i], 0.0, 1.0, (-5.0, 5.0))
        errors += abs(result)
    simann_errors.append(errors / tests)

# monte_sols = ["10", "50", "100", "1000", "5000", "10000", "50000", "100000"]
monte_sols = np.rint(np.exp(np.linspace(3, 15, 100))) / 2
monte_times = []
monte_errors = []

for i in range(len(monte_sols)):
    t_monte = timeit("result, vals = optimise.montecarlo(quadratic, 0, " + str(int(monte_sols[i])) + ", 1, (-5.0, 5.0))",
                     setup=setup, number=tests)
    monte_times.append(t_monte / tests)
    errors = 0
    for j in range(tests):
        result, vals = optimise.montecarlo(quadratic, 0, int(monte_sols[i]), 1, (-5.0, 5.0))
        errors += abs(result)
    monte_errors.append(errors / tests)

# monte_lhs = "result, vals = optimise.monte_lhs(quadratic, 0, 100000, 1, (-5.0, 5.0))"

# Save simann data
f = open("data/timeitFsimann.dat", "wb")
pickle.dump((simann_decs, simann_errors, simann_times), f, True)
f.close()

# Save montecarlo data
f = open("data/timeitFmonte.dat", "wb")
pickle.dump((monte_sols, monte_errors, monte_times), f, True)
f.close()

# t_monte = timeit(monte, setup=setup, number=10)
# t_monte_lhs = timeit(monte_lhs, setup=setup, number=10)
# print("Simulated annealing: ", t_simann)
# print("Monte Carlo: ", t_monte)
# print("Monte Carlo with LHS: ", t_monte_lhs)
