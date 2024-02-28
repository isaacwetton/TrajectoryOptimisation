import numpy as np


def simann(func, increase, decrease, target, temp, *spaces, track_evolution=False):
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

    # Create lists for tracking tested combinations
    if track_evolution:
        tested = []

    # Run optimisation until temperature reaches zero
    while temp > 0:
        # Test new values and adjust temperature accordingly
        result = func(*vals)

        # Add values and result to tracked tests
        if track_evolution:
            tested.append([*vals, result])

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

        print("Temperature: " + str(temp))

        # Define new values
        for i in range(0, len(vals)):
            vals[i] = vals0[i] + np.random.uniform(low=-space_sizes[i] * temp, high=space_sizes[i] * temp)
            while not spaces[i][0] <= vals[i] <= spaces[i][1]:
                vals[i] = vals0[i] + np.random.uniform(low=-space_sizes[i] * temp, high=space_sizes[i] * temp)

    if not track_evolution:
        return best, vals0
    else:
        return best, vals0, tested


def montecarlo(func, target, sols_no, multistages, *spaces):
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

    # Multistage steps
    space_reduction = 1
    if multistages > 0:
        for multistage in range(multistages):
            # Reduce search space
            space_reduction *= 0.1
            # Define new set of sample points
            sols = []
            for solution in range(sols_no):
                sol_vals = vals.copy()
                for i in range(0, len(vals)):
                    sol_vals[i] = np.random.uniform(low=values[i] - space_sizes[i] * space_reduction,
                                                    high=values[i] + space_sizes[i] * space_reduction)
                sols.append(sol_vals)

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


def monte_lhs(func, target, sols_no, multistages, *spaces):
    var_no = len(spaces)

    # Space sizes
    space_sizes = [None] * var_no
    for i in range(0, len(spaces)):
        space_sizes[i] = spaces[i][1] - spaces[i][0]

    # Create set of feasible variable values
    pos_val = [None] * var_no
    for i in range(var_no):
        pos_val[i] = np.linspace(spaces[i][0], spaces[i][1], sols_no)

    # Create set of possible solutions
    sols = []
    for i in range(sols_no):
        sol_vals = [None] * var_no
        for j in range(0, var_no):
            k = np.random.randint(0, len(pos_val[j]))
            sol_vals[j] = pos_val[j][k]
            temp = np.delete(pos_val[j], k)
            pos_val[j] = temp
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

    # # Multistage steps
    # space_reduction = 1
    # for multistage in range(multistages):
    #     # Reduce search space
    #     space_reduction *= 0.1
    #     # Define new set of sample points
    #     sols = []
    #     for solution in range(sols_no):
    #         sol_vals = vals.copy()
    #         for i in range(0, len(vals)):
    #             sol_vals[i] = np.random.uniform(low=values[i] - space_sizes[i] * space_reduction,
    #                                             high=values[i] + space_sizes[i] * space_reduction)
    #         sols.append(sol_vals)
    #
    #     # Test solutions and output result
    #     for solution in sols:
    #         result = func(*solution)
    #         if best is None:
    #             best = result
    #             values = solution
    #         elif abs(result - target) < abs(best - target):
    #             best = result
    #             values = solution

    return best, values
