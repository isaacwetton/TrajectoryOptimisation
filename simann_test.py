import optimise


# Define quadratic function with single root (-0.5)
def quadratic(x):
    return 4 * x * x + 4 * x + 1


# Run simulated annealing on function
print("Test of simulated annealing:")
result, vals = optimise.simann(quadratic, 0.1, 0.00001, 0.0, 1.0, (-5.0, 5.0))
print("The best result was " + str(result))
print("This was found using x = " + str(vals[0]))

# Run Monte Carlo on function
print("\nTest of Monte Carlo:")
result, vals = optimise.montecarlo(quadratic, 0, 100000, (-5.0, 5.0))
print("The best result was " + str(result))
print("This was found using x = " + str(vals[0]))