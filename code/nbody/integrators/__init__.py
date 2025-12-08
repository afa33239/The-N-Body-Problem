## this is an interface for different integrators to implement

from typing import Callable
from nbody.bodies import SystemState


class Integrator:

    def step(
        self,
        state: SystemState,
        cfg: "SimulationConfig",   # quoted to avoid import
        accel_fn: Callable
    ) -> SystemState:
        raise NotImplementedError()