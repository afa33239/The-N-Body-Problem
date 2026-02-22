from code.nbody.bodies import Body, SystemState
from code.nbody.integrators import Integrator


class LeapfrogIntegrator(Integrator):
    """
    Leapfrog (kick-drift) integrator.

    Stores velocities at half-steps internally (v_{n+1/2}).
    synchronize() converts to full-step velocities for diagnostics.
    """

    def initialize(self, state: SystemState, cfg, accel_fn) -> SystemState:
        """
        Prepares the integrator state for stepping.

        For leapfrog, this moves velocities to the half-step:
        v^{1/2} = v^0 + 0.5*dt*a(x^0)
        """
        bodies = state.bodies
        dt = cfg.dt

        ax, ay, az = accel_fn(bodies)

        new_bodies = []
        for i, b in enumerate(bodies):
            vx = b.vx + 0.5 * dt * ax[i]
            vy = b.vy + 0.5 * dt * ay[i]
            vz = b.vz + 0.5 * dt * az[i]
            new_bodies.append(Body(b.m, b.x, b.y, b.z, vx, vy, vz))

        return SystemState(new_bodies, accel=(ax, ay, az))

    def step(self, state: SystemState, cfg, accel_fn) -> SystemState:
        """
        Advances the system by one timestep using leapfrog.

        - Drift positions using half-step velocities
        - Compute new accelerations
        - Kick velocities forward by one full dt
        """
        bodies = state.bodies
        dt = cfg.dt

        drifted = []
        for b in bodies:
            x = b.x + dt * b.vx
            y = b.y + dt * b.vy
            z = b.z + dt * b.vz
            drifted.append(Body(b.m, x, y, z, b.vx, b.vy, b.vz))

        ax, ay, az = accel_fn(drifted)

        new_bodies = []
        for i, b in enumerate(drifted):
            vx = b.vx + dt * ax[i]
            vy = b.vy + dt * ay[i]
            vz = b.vz + dt * az[i]
            new_bodies.append(Body(b.m, b.x, b.y, b.z, vx, vy, vz))

        return SystemState(new_bodies, accel=(ax, ay, az))

    def synchronize(self, state: SystemState, cfg, accel_fn) -> SystemState:
        """
        Produces a "measurement state" for diagnostics.

        Leapfrog stores v at half steps, so this converts:
        v^n = v^{n+1/2} - 0.5*dt*a(x^n)
        """
        bodies = state.bodies
        dt = cfg.dt

        if state.accel is not None:
            ax, ay, az = state.accel
        else:
            ax, ay, az = accel_fn(bodies)

        synced = []
        for i, b in enumerate(bodies):
            vx = b.vx - 0.5 * dt * ax[i]
            vy = b.vy - 0.5 * dt * ay[i]
            vz = b.vz - 0.5 * dt * az[i]
            synced.append(Body(b.m, b.x, b.y, b.z, vx, vy, vz))

        return SystemState(synced)