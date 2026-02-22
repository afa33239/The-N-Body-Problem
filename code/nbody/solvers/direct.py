from code.nbody.solvers import Solver
from code.nbody.physics import compute_accelerations


class DirectSolver(Solver):
    """
    Direct O(N^2) solver.

    Computes pairwise gravitational interactions between all bodies.
    """

    def accelerations(self, bodies, cfg):
        # delegate to physics module
        return compute_accelerations(bodies, cfg)