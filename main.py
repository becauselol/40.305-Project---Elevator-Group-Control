import time
import numpy as np
import random
import pandas as pd
from simulation.classes.sim import Simulation
import simulation.classes.groupController as gControl

from analysis.homogeneous.analysis import print_res, convert_to_reward, calculate_expected_reward, plt_graph, overall_stat, plt_comparison

if __name__ == "__main__":
    print("RUNNING VARIOUS SIMULATIONS\n")

    print("RUNNING")
    # Seed for randomness
    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    
    simulation_data = []
    result_wait_t = []
    result_idle_t = []
    params = {
            "num_floors": 6,
            "num_elevators": 3,
            "total_arrival_rate": 0.6,
            "simulation_duration": 72000
            "idle_floor": [1] * 3
            }
    
    print("random seed:", seed)
    print("simulation duration:", params["simulation_duration"])
    print("number of floors:", params["num_floors"])
    print("number of elevators:", params["num_elevators"])

    zoning_params = {
            1: [1, 2],
            2: [3, 4],
            3: [5, 6]
            }

    result_random = run_experiemnt(params, RandomController)
    result_zoning = run_experiemnt(params, ZoningController, zoning_params)
    result_nearest = run_experiemnt(params, NearestElevatorController)

    for floor, rewards in reward_dict["wait_time"].items():
        num_passengers = reward_dict["num_passenger"][floor]
        result = calculate_expected_reward(num_passengers, rewards)
        result["floor"] = floor
        result_wait_t.append(result)
        print_res(result, f"wait time for floor {floor}")

    wait_time_data = pd.DataFrame(result_wait_t)

    for floor, rewards in reward_dict["num_passenger"].items():
        result = calculate_expected_reward(cycle_len_arr, rewards)
        print_res(result, f"arrival rate for floor {floor}")

    for elevator_id, rewards in reward_dict["idle_time"].items():
        result = calculate_expected_reward(cycle_len_arr, rewards)
        result["elevator"] = elevator_id
        result_idle_t.append(result)
        print_res(result, f"idle time for elevator {elevator_id}")
    idle_time_data = pd.DataFrame(result_idle_t)

    
    overall_stat(idle_time_data, wait_time_data)


    plt_graph(wait_time_data, "wait_time")
    plt_graph(idle_time_data, "idle_time")


    ### plot comparison graphs
    print(wait_time_data)
    plt_comparison(wait_time_data)
