import numpy as np
import random
from simulation import Simulation

random.seed(1)
np.random.seed(1)
num_floors = 4
sim = Simulation(num_floors)

for idx, cycle_data in enumerate(sim.simulate(24 * 60 * 5)):
    print("cycle:", idx)
    print(cycle_data.passengers.head())
