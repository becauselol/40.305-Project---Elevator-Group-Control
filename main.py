# HELPs recognize this as the main folder in the package
import time
import numpy as np
import random
from simulation.classes.sim import Simulation

from analysis.homogeneous.analysis import print_res, convert_to_reward, calculate_expected_reward

if __name__ == "__main__":
    print("INITIALIZING SIMULATION\n")
    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    num_floors = 4
    num_elevators = 2
    simulation_duration = 72000
    sim = Simulation(num_floors)

    print("random seed:", seed)
    print("simulation duration:", simulation_duration)
    print("number of floors:", num_floors)

    start_time = time.time()
    print(f"\nSTARTING SIMULATION\n")
    
    simulation_data = []


    for idx, cycle_data in enumerate(sim.simulate(simulation_duration)):
        # print("cycle:", idx)
        # print("cycle duration:", cycle_data.cycle_duration)
        simulation_data.append(cycle_data)
        

    end_time = time.time()
    print(f"ENDING SIMULATION\n")
    print(f"EXECUTION TIME: {end_time - start_time:6.2f}s\n")


    print("Total Number of Cycles:", len(simulation_data))

    cycle_len_arr, reward_dict = convert_to_reward(simulation_data, num_floors, num_elevators)

    for floor, rewards in reward_dict["wait_time"].items():
        num_passengers = reward_dict["num_passenger"][floor]
        result = calculate_expected_reward(num_passengers, rewards)
        print_res(result, f"wait time for floor {floor}")

    for floor, rewards in reward_dict["num_passenger"].items():
        result = calculate_expected_reward(cycle_len_arr, rewards)
        print_res(result, f"arrival rate for floor {floor}")

    for elevator_id, rewards in reward_dict["idle_time"].items():
        result = calculate_expected_reward(cycle_len_arr, rewards)
        print_res(result, f"idle time for elevator {elevator_id}")
