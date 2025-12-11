from code.nbody.bodies import Body, SystemState
from code.nbody.integrators import Integrator


class LeapfrogIntegrator(Integrator): 

    def step(self, state, cfg, accel_fn):
        
        bodies = state.bodies
        dt = cfg.dt

        # 1) compute a_old
        ax_old, ay_old = accel_fn(bodies) #cfg is still called internally 

        # We'll store updated bodies 
        temp_bodies = []

        #half-step velocity update + FULL position update
        for i, b in enumerate(bodies):
            # half-step velocity
            vhx = b.vx + 0.5 * dt * ax_old[i]
            vhy = b.vy + 0.5 * dt * ay_old[i]

            # position update
            new_x = b.x + dt * vhx
            new_y = b.y + dt * vhy

            temp_bodies.append(Body(b.m, new_x, new_y, vhx, vhy)) #appends the body with UPDATED position but OLD half-step velocity

        # compute a_new from UPDATED positions
        ax_new, ay_new = accel_fn(temp_bodies)

        # second half-step velocity update
        new_bodies = []
        for i, b in enumerate(temp_bodies):
            vx_new = b.vx + 0.5 * dt * (ax_old[i] + ax_new[i])
            vy_new = b.vy + 0.5 * dt * (ay_old[i] + ay_new[i])
            new_bodies.append(Body(b.m, b.x, b.y, vx_new, vy_new))

        return SystemState(new_bodies)



