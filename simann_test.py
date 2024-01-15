import optimise


# Define quadratic function with single root (-0.5)
def quadratic(x):
    return 4 * x * x + 4 * x + 1


# Run simulated annealing on function
result, vals = optimise.simann(quadratic, 0.1, 0.00001, 0.0, 1.0, (-5.0, 5.0))
print("The best result was " + str(result))
print("This was found using x = " + str(vals[0]))
