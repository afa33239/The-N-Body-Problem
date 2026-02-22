from code.nbody.solvers import Solver
from code.nbody.trees.octree import OctreeNode


class BarnesHutSolver(Solver):
    """
    Barnes–Hut solver using a 3D octree.

    Uses an opening angle parameter (theta) to decide when to
    approximate a group of bodies as a single mass.
    """

    def __init__(self, theta: float = 0.7):
        """
        theta: opening angle controlling accuracy vs speed.
        Smaller theta = more accurate but slower.
        """
        self.theta = theta

    def accelerations(self, bodies, cfg):
        """
        Computes gravitational accelerations for all bodies
        using the Barnes–Hut approximation.

        Returns three lists: ax, ay, az.
        """
        N = len(bodies)

        ax = [0.0] * N
        ay = [0.0] * N
        az = [0.0] * N

        # Build a bounding cube that contains all bodies
        xs = [b.x for b in bodies]
        ys = [b.y for b in bodies]
        zs = [b.z for b in bodies]

        cx = 0.5 * (min(xs) + max(xs))
        cy = 0.5 * (min(ys) + max(ys))
        cz = 0.5 * (min(zs) + max(zs))

        size = max(
            max(xs) - min(xs),
            max(ys) - min(ys),
            max(zs) - min(zs),
        )

        # small padding prevents zero-size cube edge cases
        half_size = 0.5 * size + 1e-10

        root = OctreeNode((cx, cy, cz), half_size)

        # Insert all bodies into the octree
        for b in bodies:
            root.insert(b)

        # Compute acceleration for each body
        for i, b in enumerate(bodies):
            ax[i], ay[i], az[i] = root.compute_accelerations(
                b,
                self.theta,
                cfg.softening,
            )

        return ax, ay, az