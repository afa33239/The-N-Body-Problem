import time
import random

from code.nbody.bodies import Body
from code.nbody.engine import Simulation, SimulationConfig
from code.nbody.integrators.leapfrog import LeapfrogIntegrator
from code.nbody.solvers.direct import DirectSolver
from code.nbody.solvers.barneshut import BarnesHutSolver


def make_random_bodies(N, seed=0, pos_scale=1.0, vel_scale=0.5,
                       m_min=1e-3, m_max=1e-2):
    random.seed(seed)
    bodies = []
    for _ in range(N):
        bodies.append(Body(
            m=random.uniform(m_min, m_max),
            x=random.uniform(-pos_scale, pos_scale),
            y=random.uniform(-pos_scale, pos_scale),
            z=random.uniform(-pos_scale, pos_scale),
            vx=random.uniform(-vel_scale, vel_scale),
            vy=random.uniform(-vel_scale, vel_scale),
            vz=random.uniform(-vel_scale, vel_scale),
        ))
    return bodies


def time_simulation(bodies, solver, dt, steps, softening):
    cfg = SimulationConfig(dt=dt, timesteps=steps, softening=softening)
    sim = Simulation(
        bodies=bodies,
        cfg=cfg,
        integrator=LeapfrogIntegrator(),
        solver=solver,
    )

    MAX = 180 # seconds

    t0 = time.perf_counter()
    try:
        sim.run()
    except KeyboardInterrupt:
        pass
    elapsed = time.perf_counter() - t0

    if elapsed > MAX:
        raise TimeoutError(f"Simulation exceeded maximum time of {MAX} seconds.")   

    return elapsed, sim


