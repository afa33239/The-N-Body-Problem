## holds configurations of the simulation & simulation itself and runs it


import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List

from code.nbody.bodies import Body, SystemState

from code.nbody.integrators.euler import EulerIntegrator

from code.nbody.solvers.direct import DirectSolver

from code.nbody.physics import compute_kinetic_energy, compute_potential_energy, compute_angular_momentum


class SimulationConfig: 

    def __init__(self, dt, timesteps, softening=0.001):
        self.dt = dt
        self.timesteps = timesteps
        self.softening = softening


class Simulation:

    def __init__(self, bodies: List[Body], cfg: SimulationConfig, integrator=None, solver=None):
        self.state = SystemState(bodies)
        self.cfg = cfg
        self.integrator = integrator or EulerIntegrator()
        self.solver = solver or DirectSolver()

        self.energy_history = []  #keeps track of energies and angular momentum
        self.kinetic_history = []
        self.potential_history = []
        self.energy_drift = [] #this is used to track relative energy drift over time 
        self.angular_momentum_history = []

    def run(self):
       
        self.state_history = [] #create state history


        self.state_history.append(self.state.copy()) #save deep copy of initial state


        pss = []

        ps = [(b.x, b.y) for b in self.state.bodies]
        pss.append(ps)

        for t in range(self.cfg.timesteps):
            # delegate time-stepping to the integrator#
            
            def accel_fn(bodies): #this is just a wrapper function
                return self.solver.accelerations(bodies, self.cfg)

            self.state = self.integrator.step(
                self.state,
                self.cfg,
                accel_fn
            )
            ps = [(b.x, b.y) for b in self.state.bodies]
            pss.append(ps)

            self.state_history.append(self.state.copy())



            #energy
            K = compute_kinetic_energy(self.state.bodies)
            self.kinetic_history.append(K)
            U = compute_potential_energy(self.state.bodies, self.cfg)
            self.potential_history.append(U)

            E = K + U
            self.energy_history.append(E)

            if t == 0: 
                self.E0 = E
            self.energy_drift.append((E - self.E0) / abs(self.E0)) #energy drift implemented


            #angular momentum
            L = compute_angular_momentum(self.state.bodies)
            self.angular_momentum_history.append(L)

        

        return pss

    def closestDistance(self):
        import math

        ret = None
        pss = self.run()

        for step in pss:
            for a in step:
                for b in step:
                    if a is not b:
                        d = a.squareDist(b)
                        if ret is None or d < ret:
                            ret = d

        return None if ret is None else math.sqrt(ret)

    def show(self, x0, y0, x1, y1):
       
        pss = self.run()

        fig, ax = plt.subplots()
        ax.set_xlim(x0, x1)
        ax.set_ylim(y0, y1)

        scatters = [
            ax.scatter([], [], label=f"Body {i}")
            for i in range(len(self.state.bodies))
        ]

        time_text = ax.text(
            0.02, 0.98, '',
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )

        def update(frame):
            for i, sc in enumerate(scatters):
                sc.set_offsets([pss[frame][i].x, pss[frame][i].y])
            time_text.set_text(f"Timestep: {frame}")
            return scatters + [time_text]

        FuncAnimation(
            fig, update,
            frames=len(pss),
            interval=1,
            blit=True,
            repeat=False
        )

        ax.set_xlabel("X coordinate (AU)")
        ax.set_ylabel("Y coordinate (AU)")
        ax.set_title("Celestial Body Trajectories")
        ax.legend()
        plt.show()