# HELPs recognize this as the main folder in the package
import numpy as np
import random
from simulation.classes.sim import Simulation

from analysis.homogeneous.analysis import print_res, convert_to_reward, calculate_expected_reward

if __name__ == "__main__":
    print("INITIALIZING SIMULATION")
    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    num_floors = 4
    simulation_duration = 72000
    sim = Simulation(num_floors)

    print("random seed:", seed)
    print("simulation duration:", simulation_duration)
    print("number of floors:", num_floors)

    print("STARTING SIMULATION")
    
    simulation_data = []

    for idx, cycle_data in enumerate(sim.simulate(simulation_duration)):
        # print("cycle:", idx)
        # print("cycle duration:", cycle_data.cycle_duration)
        simulation_data.append(cycle_data)

    print("Total Number of Cycles:", len(simulation_data))

    cycle_len_arr, reward_dict = convert_to_reward(simulation_data)

    for reward, values in reward_dict.items():
        result = calculate_expected_reward(cycle_len_arr, values)

        print_res(result, reward)

