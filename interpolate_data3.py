"""Interpolate the master data file to a common average
"""
import pickle

import numpy as np

# Load data
f = open("data/targeting1data1.dat", "rb")
orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, lats, lons = pickle.load(f)
f.close()

# Get orbiterpositions
print("Loading orbiter")
orbpos = np.array(orbpos)

# Get Satellite positions
print("Loading callisto")
calpos = np.array(calpos)

print("Loading ganymede")
ganpos = np.array(ganpos)

print("Loading europa")
eurpos = np.array(eurpos)

print("Loading io")
iopos = np.array(iopos)

print("getting times")
t_start_of_mission = np.array(times) - times[0]
new_times = np.arange(np.min(t_start_of_mission), np.max(t_start_of_mission)+60.0, 60.0)

# Now interpolate to the same 60 second time resolution
orbxpos = np.interp(new_times, t_start_of_mission, orbpos[:,0])
orbypos = np.interp(new_times, t_start_of_mission, orbpos[:,1])
calxpos = np.interp(new_times, t_start_of_mission, calpos[:,0])
calypos = np.interp(new_times, t_start_of_mission, calpos[:,1])
ganxpos = np.interp(new_times, t_start_of_mission, ganpos[:,0])
ganypos = np.interp(new_times, t_start_of_mission, ganpos[:,1])
eurxpos = np.interp(new_times, t_start_of_mission, eurpos[:,0])
eurypos = np.interp(new_times, t_start_of_mission, eurpos[:,1])
ioxpos = np.interp(new_times, t_start_of_mission, iopos[:,0])
ioypos = np.interp(new_times, t_start_of_mission, iopos[:,1])
times = np.interp(new_times, t_start_of_mission, times)

fout = open("data/targeting1data1_pickle.pickle", "wb")
pickle.dump([orbxpos, orbypos,
             calxpos, calypos,
             ganxpos, ganypos,
             eurxpos, eurypos,
             ioxpos, ioypos,
             times], fout, protocol=pickle.HIGHEST_PROTOCOL)
f.close()