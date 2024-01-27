import pickle
from matplotlib import pyplot as plt

# Load simann data
f = open("data/timeit3simann.dat", "rb")
simann_decs, simann_errors, simann_times = pickle.load(f)
f.close()

print(simann_times)
print(simann_decs)
# Create plot
plt.plot(simann_decs, simann_times, "k")
plt.title("A plot of runtime against temperature decrease rate\nfor simulated annealing optimisation applied to Jupiter capture")
plt.xlabel(r"Temperature decrease size")
plt.ylabel("Average test runtime (s)")
plt.show()
