import pickle
from matplotlib import pyplot as plt

# Load monte data
f = open("data/timeit4monte.dat", "rb")
monte_sols, monte_errors, monte_times = pickle.load(f)
f.close()

print(monte_sols)
print(monte_times)

# Create plot
plt.plot(monte_sols, monte_times, "k")
plt.title("A plot of runtime against sample size for single-stage\nMonte Carlo optimisation applied to Jupiter capture")
plt.xlabel(r"Number of sampled solutions")
plt.ylabel("Average test runtime (s)")
plt.show()
