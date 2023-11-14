# Import used modules
import numpy as np


# Define Particle Class
class Particle:
    """
    A class used for modelling the movement of a single particle.

    Each object of the class has a name for identification, a mass, and values for position, velocity and acceleration.
    """

    def __init__(
            self,
            position=np.array([0, 0, 0], dtype=float),
            velocity=np.array([0, 0, 0], dtype=float),
            acceleration=np.array([0, 0, 0], dtype=float),
            name='Ball',
            mu=1.0
    ):
        """Class initialisation method which sets the received arguments as object attributes"""
        self.name = name
        self.mu = mu
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.array(acceleration, dtype=float)

    def __str__(self):
        """Prints the object attributes as a string if the object is called directly"""
        return "Particle: {0}, Mass: {1:.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}".format(
            self.name, self.mass, self.position, self.velocity, self.acceleration
        )

    def update_euler(self, deltaT):
        """
        Updates position and acceleration of the particle object after a time interval of deltaT.

        Uses the Euler method.

        :param deltaT: The time step for which to update the system
        """
        # Update position
        for i in range(0, 3):
            self.position[i] = self.position[i] + (self.velocity[i] * deltaT)
        # Update velocity
        for i in range(0, 3):
            self.velocity[i] = self.velocity[i] + (self.acceleration[i] * deltaT)
        # Create copies of position and velocity arrays to ensure that all entries are floats
        self.position = np.array([self.position[0], self.position[1], self.position[2]], dtype=float)
        self.velocity = np.array([self.velocity[0], self.velocity[1], self.velocity[2]], dtype=float)

    def update_eulerCromer(self, deltaT):
        """
        Updates position and acceleration of the particle object after a time interval of deltaT.

        Uses the Euler-Cromer method.

        :param deltaT: The time step for which to update the system
        """
        # Update velocity
        for i in range(0, 3):
            self.velocity[i] = self.velocity[i] + (self.acceleration[i] * deltaT)
        # Update position
        for i in range(0, 3):
            self.position[i] = self.position[i] + (self.velocity[i] * deltaT)
        # Create copies of position and velocity arrays to ensure that all entries are floats
        self.position = np.array([self.position[0], self.position[1], self.position[2]], dtype=float)
        self.velocity = np.array([self.velocity[0], self.velocity[1], self.velocity[2]], dtype=float)

    def updateGravitationalAcceleration(self, body):
        """
        Calculates the gravitational acceleration of a body due to another body

        :param body: The second body, which causes the acceleration (Particle.py Particle object)

        :return: The value of the acceleration due to body
        """

        sep = np.linalg.norm(self.position - body.position)
        normalised_sep = (self.position - body.position) / sep
        grav_accel_mag = -body.mu / (sep**2)
        grav_accel = grav_accel_mag * normalised_sep
        return grav_accel


# Console error message if script is run directly
if __name__ == "__main__":
    print("This python script is not intended to be run independently.\n")
    input("Press the enter key to continue")