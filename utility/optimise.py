import numpy as np


def simann(func, increase, decrease, target, temp, *spaces):
    # List of variables for function
    vals = [None] * len(spaces)

    # Space sizes
    space_sizes = [None] * len(spaces)
    for i in range(0, len(spaces)):
        space_sizes[i] = spaces[i][1] - spaces[i][0]

    # Set initial values
    for i in range(0, len(vals)):
        vals[i] = np.random.uniform(low=spaces[i][0], high=spaces[i][1])
    vals0 = vals.copy()

    # Create variable for tracking of best result
    best = None

    # Run optimisation until temperature reaches zero
    while temp > 0:
        # Test new values and adjust temperature accordingly
        result = func(*vals)
        if best is None:
            best = result
        elif abs(result - target) < abs(best - target):
            best = result
            temp += increase
            vals0 = vals.copy()

        else:
            temp -= decrease

        if temp > 1.0:
            temp = 1.0

        # Define new values
        for i in range(0, len(vals)):
            vals[i] = vals0[i] + np.random.uniform(low=-space_sizes[i] * temp, high=space_sizes[i] * temp)
            while not spaces[i][0] <= vals[i] <= spaces[i][1]:
                vals[i] = vals0[i] + np.random.uniform(low=-space_sizes[i] * temp, high=space_sizes[i] * temp)

    return best, vals0

def montecarlo(func, target, sols_no, *spaces):
    # List of variables for function
    vals = [None] * len(spaces)

    # Space sizes
    space_sizes = [None] * len(spaces)
    for i in range(0, len(spaces)):
        space_sizes[i] = spaces[i][1] - spaces[i][0]

    # Create set of feasible solutions
    sols = []
    for solution in range(sols_no):
        sol_vals = vals.copy()
        for i in range(0, len(vals)):
            sol_vals[i] = np.random.uniform(low=spaces[i][0], high=spaces[i][1])
        sols.append(sol_vals)

    # Create variable for tracking of best result
    best = None
    values = None

    # Test solutions and output result
    for solution in sols:
        result = func(*solution)
        if best is None:
            best = result
            values = solution
        elif abs(result - target) < abs(best - target):
            best = result
            values = solution

    return best, values
