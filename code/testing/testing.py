from code.testing.benchmark_phase5 import make_random_bodies, time_simulation
from code.nbody.solvers.direct import DirectSolver
from code.nbody.solvers.barneshut import BarnesHutSolver
from code.nbody.bodies import Body


N = 1000
dt = 2e-3
steps = 2000
softening = 1e-3
seed = 42

bodies = make_random_bodies(N, seed=seed)

# Direct
t_direct, sim_direct = time_simulation(
    [Body(*b.asTuple()) for b in bodies],
    DirectSolver(),
    dt, steps, softening
)

# Barnes–Hut
t_bh, sim_bh = time_simulation(
    [Body(*b.asTuple()) for b in bodies],
    BarnesHutSolver(theta=1),
    dt, steps, softening
)

print(f"N={N}")
print(f"Direct runtime: {t_direct:.3f} s")
print(f"Barnes–Hut runtime: {t_bh:.3f} s")