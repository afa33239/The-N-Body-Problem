import math
from typing import List

from code.nbody.bodies import Body, SystemState
from code.nbody.integrators.euler import EulerIntegrator
from code.nbody.solvers.direct import DirectSolver
from code.nbody.physics import (
    compute_kinetic_energy,
    compute_potential_energy,
    compute_angular_momentum,
    compute_linear_momentum,
    compute_center_of_mass,
)


class SimulationConfig:
    """
    Stores all configuration parameters for a simulation run.
    """

    def __init__(self, dt, timesteps, softening=0.001):
        """
        dt: timestep size
        timesteps: number of integration steps
        softening: gravitational softening parameter
        """
        self.dt = dt
        self.timesteps = timesteps
        self.softening = softening

        # Optional features
        self.record_history = False
        self.diagnostics_every = 1
        self.enable_diagnostics = False
        self.record_frames = False
        self.frame_every = 1


class Simulation:
    """
    Main simulation engine.

    Handles:
    - integration loop
    - diagnostics
    - optional frame recording
    """

    def __init__(self, bodies: List[Body], cfg: SimulationConfig, integrator=None, solver=None):
        """
        bodies: initial list of Body objects
        cfg: SimulationConfig
        integrator: time integration method
        solver: acceleration computation method
        """
        self.state = SystemState(bodies)
        self.cfg = cfg

        self.integrator = integrator if integrator is not None else EulerIntegrator()
        self.solver = solver if solver is not None else DirectSolver()

        # histories
        self.state_history = []

        self.kinetic_history = []
        self.potential_history = []
        self.energy_history = []
        self.energy_drift = []

        self.angular_momentum_history = []
        self.angular_momentum_drift = []

        self.linear_momentum_history = []
        self.linear_momentum_drift = []

        self.com_history = []
        self.com_drift = []

        # animation frames (positions only)
        self.frames = []

    def run(self):
        """
        Runs the full simulation loop.

        Returns optional position history if record_history is enabled.
        """
        self._clear_histories()
        accel_fn = self._initialize_simulation()

        pss = None
        if self.cfg.record_history:
            pss = []
            pss.append([(b.x, b.y, b.z) for b in self.state.bodies])

        for step in range(self.cfg.timesteps):
            self._step(accel_fn, step)

            if pss is not None:
                pss.append([(b.x, b.y, b.z) for b in self.state.bodies])

        return pss

    def _initialize_simulation(self):
        """
        Prepares integrator state and computes initial diagnostics.
        """

        def accel_fn(bodies):
            return self.solver.accelerations(bodies, self.cfg)

        # Prepare integrator internal state
        self.state = self.integrator.initialize(self.state, self.cfg, accel_fn)

        # Synchronize state for measurement
        diag = self.integrator.synchronize(self.state, self.cfg, accel_fn)

        if self.cfg.record_history:
            self.state_history.append(diag.copy())

        if self.cfg.record_frames:
            self.frames.append([(b.x, b.y, b.z) for b in diag.bodies])

        if self.cfg.enable_diagnostics:
            self._update_diagnostics(diag, is_initial=True)

        return accel_fn

    def _step(self, accel_fn, step):
        """
        Advances the system by one timestep and updates diagnostics.
        """
        self.state = self.integrator.step(self.state, self.cfg, accel_fn)
        diag = self.integrator.synchronize(self.state, self.cfg, accel_fn)

        if self.cfg.record_history:
            self.state_history.append(diag.copy())

        if self.cfg.record_frames and (step + 1) % self.cfg.frame_every == 0:
            self.frames.append([(b.x, b.y, b.z) for b in diag.bodies])

        if self.cfg.enable_diagnostics and (step + 1) % self.cfg.diagnostics_every == 0:
            self._update_diagnostics(diag)

    def _update_diagnostics(self, diag, is_initial=False):
        """
        Computes and stores energy, momentum and center-of-mass diagnostics.
        """
        K = compute_kinetic_energy(diag.bodies)
        U = compute_potential_energy(diag.bodies, self.cfg)
        E = K + U

        L = compute_angular_momentum(diag.bodies)
        P = compute_linear_momentum(diag.bodies)
        x_cm, y_cm, z_cm = compute_center_of_mass(diag.bodies)

        self.kinetic_history.append(K)
        self.potential_history.append(U)
        self.energy_history.append(E)

        L_mag = math.sqrt(L[0] ** 2 + L[1] ** 2 + L[2] ** 2)
        self.angular_momentum_history.append(L_mag)

        self.linear_momentum_history.append(P)
        self.com_history.append((x_cm, y_cm, z_cm))

        if is_initial:
            self.E0 = E
            self.E_scale = max(abs(E), abs(K) + abs(U), 1e-12)
            self.energy_drift.append(0.0)
            self.angular_momentum_drift.append(0.0)
            self.linear_momentum_drift.append(0.0)
            self.com0 = (x_cm, y_cm, z_cm)
            self.L0_mag = L_mag
            self.com_drift.append(0.0)
        else:
            den = self.E_scale
            drift = abs(E - self.E0) / den if den > 0 else 0.0
            self.energy_drift.append(drift)

            if self.L0_mag > 1e-14:
                self.angular_momentum_drift.append((L_mag - self.L0_mag) / self.L0_mag)
            else:
                self.angular_momentum_drift.append(L_mag)

            self.linear_momentum_drift.append(
                math.sqrt(P[0] ** 2 + P[1] ** 2 + P[2] ** 2)
            )

            dx = x_cm - self.com0[0]
            dy = y_cm - self.com0[1]
            dz = z_cm - self.com0[2]
            self.com_drift.append(math.sqrt(dx * dx + dy * dy + dz * dz))

    def _clear_histories(self):
        """
        Clears all stored histories before a new run.
        """
        self.state_history.clear()

        self.kinetic_history.clear()
        self.potential_history.clear()
        self.energy_history.clear()
        self.energy_drift.clear()

        self.angular_momentum_history.clear()
        self.angular_momentum_drift.clear()

        self.linear_momentum_history.clear()
        self.linear_momentum_drift.clear()

        self.com_history.clear()
        self.com_drift.clear()

        self.frames.clear()