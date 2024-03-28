import pickle
import constants
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.animation import FFMpegWriter

class AnimateTrajectory:
    def __init__(self):
        """Constructor
        """
        # What units do we plot the animation in, and so what are the labels we need?
        self.plot_length_units = constants.R_JUPITER
        self.plot_length_units_label = r"[$\mathrm{R}_\mathrm{J}$]"
        self.orb_col = "k"
        self.cal_col = "tab:purple"
        self.gan_col = "tab:green"
        self.eur_col = "tab:blue"
        self.io_col = "tab:orange"

    def load_original_data(self, filename):
        """Load data from one of the original data files

                Parameters
        ----------
        filename : str
            Filename of the data file to load
        """

        # Load trajectory data
        with open(filename, "rb") as f:
            print("Loading raw data")
            orbpos, orbvel, calpos, ganpos, iopos, eurpos, semimajors, times, vels, Jdists = pickle.load(f)

            # Get orbiter x and y positions
            print("Loading orbiter")
            orbpos = np.array(orbpos)
            self.orbxpos = orbpos[:,0]
            self.orbypos = orbpos[:,1]

            # Get Callisto x and y positions
            print("Loading callisto")
            calpos = np.array(calpos)
            self.calxpos = calpos[:,0]
            self.calypos = calpos[:,1]

            print("Loading ganymede")
            ganpos = np.array(ganpos)
            self.ganxpos = ganpos[:,0]
            self.ganypos = ganpos[:,1]

            print("Loading europa")
            eurpos = np.array(eurpos)
            self.eurxpos = eurpos[:,0]
            self.eurypos = eurpos[:,1]

            print("Loading io")
            iopos = np.array(iopos)
            self.ioxpos = iopos[:,0]
            self.ioypos = iopos[:,1]

            # Transform times into offsets from the beginning of mission
            self.t_start_of_mission = np.array(times) - times[0]
            print(self.t_start_of_mission[1]-self.t_start_of_mission[0])

            # For the last frame we drew, this stores the index into the data arrays
            # that we drew, the frame number we drew, and many data points we skipped
            # per frame to speed up the drawing.
            self.last_index = 0
            self.last_frame_number = 0
            self.last_scale = self.compute_scale_from_index(0)

    def load_interpolated_data(self, filename):
        # Load trajectory data
        with open(filename, "rb") as f:
            print("Loading raw data")
            self.orbxpos, self.orbypos, self.calxpos, self.calypos, self.ganxpos, self.ganypos, self.eurxpos, self.eurypos, self.ioxpos, self.ioypos, times = pickle.load(f)

            # Transform times into offsets from the beginning of mission
            self.t_start_of_mission = np.array(times) - times[0]
            print(self.t_start_of_mission[1]-self.t_start_of_mission[0])

            # For the last frame we drew, this stores the index into the data arrays
            # that we drew, the frame number we drew, and many data points we skipped
            # per frame to speed up the drawing.
            self.last_index = 0
            self.last_frame_number = 0
            self.last_scale = self.compute_scale_from_index(0)

    def compute_scale_from_index(self, index):
        """This function works out how many data points should be skipped.

        Parameters
        ----------
        index : int
            The index into the data arrays.

        Returns
        -------
        int
        """
        # We do this quite simply by deciding the scalign factor depending on the distance
        # from jupiter.
        jupiter_distance = np.sqrt(self.orbxpos[index]**2 + self.orbypos[index]**2)
        if jupiter_distance>500*constants.R_JUPITER:
            return 1000.0
        elif jupiter_distance>200*constants.R_JUPITER and jupiter_distance<=500*constants.R_JUPITER:
            return 500
        elif jupiter_distance>100*constants.R_JUPITER and jupiter_distance<=200*constants.R_JUPITER:
            return 200
        elif jupiter_distance>50*constants.R_JUPITER and jupiter_distance<=100*constants.R_JUPITER:
            return 100
        elif jupiter_distance<=50*constants.R_JUPITER:
            return 50

    def setup_figure(self, figsize=(8, 6)):
        """Setup the figure
        """
        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot()

    def compute_index_from_frame_number(self, frame_number):
        """This function works out what index into the data we should draw.

        Parameters
        ----------
        frame_number : int
        """
        # First we work out the change in frame from the last frame
        delta_frame_num = frame_number - self.last_frame_number

        # Using the index from the last frame, let's work out how how we scale
        # from frames to indices:
        new_scale = self.compute_scale_from_index(self.last_index)

        # This then tells us what the change in index is going to be, so we can
        # work out our new index.
        i = int(delta_frame_num*new_scale) + self.last_index

        print("f={} df={} i={} scale={}".format(frame_number, delta_frame_num, i, new_scale))

        # Store these for the next time we draw.
        self.last_scale = new_scale
        self.last_index = i
        self.last_frame_number = frame_number

        return i

    def anim_function(self, frame_number):
        """This is the animation function called by FuncAnimation
        """

        # Get the lower end of the indices to draw.
        i = self.compute_index_from_frame_number(frame_number)
        min_i = max(i-1000, 0)

        # Set up plot
        self.ax.cla()
        self.ax.set_title("Frame={} Index={} Time={:5.1f} hours Scale={}".format(frame_number, i, self.t_start_of_mission[i]/3600, self.last_scale))
        self.ax.add_artist(patches.Circle((0,0), constants.R_JUPITER/self.plot_length_units, ec="red", fc="orange"))
        self.ax.add_artist(patches.Circle((0,0), constants.A_CALLISTO/self.plot_length_units, ec=self.cal_col, fc="none", alpha=0.25))
        self.ax.add_artist(patches.Circle((0,0), constants.A_GANYMEDE/self.plot_length_units, ec=self.gan_col, fc="none", alpha=0.25))
        self.ax.add_artist(patches.Circle((0,0), constants.A_EUROPA/self.plot_length_units, ec=self.eur_col, fc="none", alpha=0.25))
        self.ax.add_artist(patches.Circle((0,0), constants.A_IO/self.plot_length_units, ec=self.io_col, fc="none", alpha=0.25))

        # Plot orbiter.
        self.ax.plot(self.orbxpos[min_i:i]/self.plot_length_units, self.orbypos[min_i:i]/self.plot_length_units, label="Orbiter", c=self.orb_col)
        self.ax.add_artist(patches.Circle((self.orbxpos[i]/self.plot_length_units, self.orbypos[i]/self.plot_length_units),
                                          0.5*constants.R_JUPITER/self.plot_length_units, ec="k", fc="k"))

        # Plot satellites.
        self.ax.plot(self.calxpos[min_i:i]/self.plot_length_units, self.calypos[min_i:i]/self.plot_length_units, label="Callisto", c=self.cal_col)
        self.ax.add_artist(patches.Circle((self.calxpos[i]/self.plot_length_units, self.calypos[i]/self.plot_length_units),
                                          0.5*constants.R_JUPITER/self.plot_length_units, ec=self.cal_col, fc=self.cal_col))
        self.ax.plot(self.ganxpos[min_i:i]/self.plot_length_units, self.ganypos[min_i:i]/self.plot_length_units, label="Ganymede", c=self.gan_col)
        self.ax.add_artist(patches.Circle((self.ganxpos[i]/self.plot_length_units, self.ganypos[i]/self.plot_length_units),
                                          0.5*constants.R_JUPITER/self.plot_length_units, ec=self.gan_col, fc=self.gan_col))
        self.ax.plot(self.eurxpos[min_i:i]/self.plot_length_units, self.eurypos[min_i:i]/self.plot_length_units, label="Europa", c=self.eur_col)
        self.ax.add_artist(patches.Circle((self.eurxpos[i]/self.plot_length_units, self.eurypos[i]/self.plot_length_units),
                                          0.5*constants.R_JUPITER/self.plot_length_units, ec=self.eur_col, fc=self.eur_col))
        self.ax.plot(self.ioxpos[min_i:i]/self.plot_length_units, self.ioypos[min_i:i]/self.plot_length_units, label="Io", c=self.io_col)
        self.ax.add_artist(patches.Circle((self.ioxpos[i]/self.plot_length_units, self.ioypos[i]/self.plot_length_units),
                                          0.5*constants.R_JUPITER/self.plot_length_units, ec=self.io_col, fc=self.io_col))

        # Set the limits - this code tries to centre the view on the spacecraft - so that the plot
        # moves with it.
        miny = min(self.orbypos[i]-100*constants.R_JUPITER, -100*constants.R_JUPITER)
        maxy = miny + 200*constants.R_JUPITER
        minx = min(self.orbxpos[i]-40*constants.R_JUPITER, -40*constants.R_JUPITER)
        maxx = minx + 80*constants.R_JUPITER
        self.ax.set_xlim([minx/self.plot_length_units, maxx/self.plot_length_units])
        self.ax.set_ylim([miny/self.plot_length_units, maxy/self.plot_length_units])

        # Set the labels and aspect ratio.
        self.ax.set_xlabel(r"x "+self.plot_length_units_label)
        self.ax.set_ylabel(r"y "+self.plot_length_units_label)
        self.ax.set_aspect("equal")

    def animate(self):
        """Do the animation"""
        max_frames = self.get_max_frames()
        return FuncAnimation(self.fig, self.anim_function,
                    repeat=False,
                    frames=max_frames, interval=1)

    def get_max_frames(self):
        frame = 0
        while self.last_index<len(self.t_start_of_mission):
            self.compute_index_from_frame_number(frame)
            frame += 1

        self.last_index = 0
        self.last_frame_number = 0
        self.last_scale = self.compute_scale_from_index(0)

        return frame-1

#animtraj = AnimateTrajectory("gam7data2_short.pickle")
animtraj = AnimateTrajectory()
animtraj.load_interpolated_data("data/targeting2data1_pickle.pickle")
animtraj.setup_figure()
ani = animtraj.animate()
plt.show()
# #Save animation as .gif file
# writer = PillowWriter(fps=30,
#                       metadata=dict(),
#                       bitrate=1800
#                       )
# ani.save('trajectory.gif', writer=writer)

# # Save animation as .mp4 file
# writer = FFMpegWriter(fps=60)
# ani.save('Plots + Animations/contour3ani.mp4', writer=writer)