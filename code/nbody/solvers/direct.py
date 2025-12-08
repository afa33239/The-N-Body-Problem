##simplest solver, will change later

from nbody.solvers import Solver
from nbody.physics import compute_accelerations

class DirectSolver(Solver):
    def accelerations(self, bodies, cfg):
        return compute_accelerations(bodies)