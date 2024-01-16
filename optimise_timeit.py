from timeit import timeit

setup = """
import optimise

def quadratic(x):
    return 4 * x * x + 4 * x + 1
"""

simann = "result, vals = optimise.simann(quadratic, 0.1, 0.00001, 0.0, 1.0, (-5.0, 5.0))"
monte = "result, vals = optimise.montecarlo(quadratic, 0, 100000, 1, (-5.0, 5.0))"
monte_lhs = "result, vals = optimise.monte_lhs(quadratic, 0, 100000, 1, (-5.0, 5.0))"

t_simann = timeit(simann, setup=setup, number=10)
t_monte = timeit(monte, setup=setup, number=10)
t_monte_lhs = timeit(monte_lhs, setup=setup, number=10)
print("Simulated annealing: ", t_simann)
print("Monte Carlo: ", t_monte)
print("Monte Carlo with LHS: ", t_monte_lhs)

