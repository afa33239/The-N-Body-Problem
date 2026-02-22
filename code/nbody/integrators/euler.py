from code.nbody.bodies import Body, SystemState
from code.nbody.integrators import Integrator


class EulerIntegrator(Integrator):
    """
    Forward Euler integrator (simple, but can drift in energy over long runs).
    """

    def step(self, state: SystemState, cfg, accel_fn):
        bodies = state.bodies
        dt = cfg.dt

        # accelerations at current positions
        ax, ay, az = accel_fn(bodies)

        new_bodies = []
        for i, b in enumerate(bodies):
            vx = b.vx + dt * ax[i]
            vy = b.vy + dt * ay[i]
            vz = b.vz + dt * az[i]

            x = b.x + dt * b.vx
            y = b.y + dt * b.vy
            z = b.z + dt * b.vz

            new_bodies.append(Body(b.m, x, y, z, vx, vy, vz))

        return SystemState(new_bodies)

    def initialize(self, state: SystemState, cfg, accel_fn):
        # Euler doesn't need any special setup
        return state

    def synchronize(self, state: SystemState, cfg, accel_fn):
        # Euler doesn't have half-step velocities, so nothing to sync
        return state