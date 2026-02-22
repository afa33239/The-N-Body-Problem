import math
from typing import List


# Gravitational constant (AU^3 / (M_sun * yr^2))
G = 4 * (math.pi ** 2)


class Body:
    """
    Represents a single body in the simulation.
    Stores mass, position, and velocity components.
    """

    def __init__(self, m, x, y, z=0.0, vx=0.0, vy=0.0, vz=0.0):
        """
        m: mass
        x, y, z: position
        vx, vy, vz: velocity
        """
        self.m = m
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def squareDist(self, other: "Body"):
        """
        Returns the squared distance to another body.
        """
        return (
            (self.x - other.x) ** 2 +
            (self.y - other.y) ** 2 +
            (self.z - other.z) ** 2
        )

    def asTuple(self):
        """
        Returns the body data as a tuple.
        Useful for saving or debugging.
        """
        return (self.m, self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def __repr__(self):
        """
        String representation of the body.
        """
        return (
            f"Body({self.m}, {self.x}, {self.y}, {self.z}, "
            f"{self.vx}, {self.vy}, {self.vz})"
        )


class SystemState:
    """
    Stores the full system state at a given timestep.

    bodies: list of Body objects
    accel: optional stored accelerations (used by Leapfrog)
    """

    def __init__(self, bodies: List[Body], accel=None):
        """
        bodies: list of Body objects
        accel: tuple (ax, ay, az) or None
        """
        self.bodies = bodies
        self.accel = accel

    def copy(self):
        """
        Returns a deep copy of the system state.
        """
        new_state = SystemState([
            Body(b.m, b.x, b.y, b.z, b.vx, b.vy, b.vz)
            for b in self.bodies
        ])

        if self.accel is not None:
            ax, ay, az = self.accel
            new_state.accel = (ax[:], ay[:], az[:])

        return new_state