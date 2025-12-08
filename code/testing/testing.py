from nbody.bodies import Body
from nbody.engine import Simulation, SimulationConfig

b1 = Body(1.0, 0.0, 0.0, 0, 1)
b2 = Body(1.0, 1.0, 0.0, 0, -1)

cfg = SimulationConfig(total_time=0.1, dt=0.01)
sim = Simulation([b1, b2], cfg)
traj = sim.run()

print(len(traj))          # should be cfg.timesteps + 1
print(traj[0][0], traj[1][0])