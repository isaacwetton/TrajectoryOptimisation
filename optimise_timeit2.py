from timeit import timeit
import optimise

def quadratic(x):
    return 4 * x * x + 4 * x + 1


setup = """
import optimise

def quadratic(x):
    return 4 * x * x + 4 * x + 1
"""

simann_decs = ["0.1", "0.01", "0.001", "0.0005", "0.0001", "0.00005", "0.00001", "0.000005"]
simann_times = []
simann_errors = []

monte = "result, vals = optimise.montecarlo(quadratic, 0, 100000, 10, (-5.0, 5.0))"
monte_lhs = "result, vals = optimise.monte_lhs(quadratic, 0, 100000, 1, (-5.0, 5.0))"

for i in range(len(simann_decs)):
    t_simann = timeit("result, vals = optimise.simann(quadratic, 0.1, " + simann_decs[i] + ", 0.0, 1.0, (-5.0, 5.0))", setup=setup, number=10)
    simann_times.append(t_simann)
    errors = 0
    for j in range(10):
        result, vals = optimise.simann(quadratic, 0.1, float(simann_decs[i]), 0.0, 1.0, (-5.0, 5.0))
        errors += abs(result)
    simann_errors.append(errors / 10)

print(simann_decs)
print(simann_errors)
print(simann_times)



# t_monte = timeit(monte, setup=setup, number=10)
# t_monte_lhs = timeit(monte_lhs, setup=setup, number=10)
# print("Simulated annealing: ", t_simann)
# print("Monte Carlo: ", t_monte)
# print("Monte Carlo with LHS: ", t_monte_lhs)

