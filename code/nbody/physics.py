
## This computes the gravitational accelerations + energies on each body due to all others (further physics added here)


import math
from typing import List
from code.nbody.bodies import Body, G


def compute_accelerations(bodies: List[Body], cfg): #added softening to calculate accelerations as well

    N = len(bodies)
    ax = [0.0] * N
    ay = [0.0] * N

    soft2 = cfg.softening * cfg.softening

    for i in range(N):
        bi = bodies[i]
        for j in range(N):
            if i == j:
                continue

            bj = bodies[j]
            dx = bj.x - bi.x
            dy = bj.y - bi.y
            dist2 = dx*dx + dy*dy + soft2
            dist32 = dist2 ** 1.5

            ax[i] += dx * bj.m * G / dist32
            ay[i] += dy * bj.m * G / dist32

    return ax, ay



def compute_kinetic_energy(bodies: List[Body]):
    Total = 0.0
    for b in bodies:
        Total += 0.5 * b.m * (b.vx ** 2 + b.vy ** 2)
    return Total

def compute_potential_energy(bodies: List[Body],cfg):
    total = 0.0
    length = len(bodies)

    for i in range(length):
        bi = bodies[i]
        for j in range(i + 1, length):
            bj = bodies[j]
            dx = bj.x - bi.x
            dy = bj.y - bi.y

            dist = math.sqrt(dx*dx + dy*dy + cfg.softening * cfg.softening)

            total += -G * bi.m * bj.m / dist
    return total


def compute_angular_momentum(bodies):
    total = 0.0
    for b in bodies:
        total += b.m * (b.x * b.vy - b.y * b.vx)
    return total


