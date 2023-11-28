import numpy as np
import random
from simulation import Simulation

random.seed(1)
np.random.seed(1)
sim = Simulation()

sim.simulate(10)
