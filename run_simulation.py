import simpy
from simulator import Simulator

# Create SimPy environment
env = simpy.Environment()

# Create simulator instance
sim = Simulator(env)

# Run simulation for 5 days
def run_simulation(env, sim):
    for _ in range(5):  # Simulate 5 days
        yield env.process(sim.advance_day())

# Start the simulation
env.process(run_simulation(env, sim))
env.run()
