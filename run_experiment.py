import time
import numpy as np
import random
import pandas as pd
from simulation.classes.sim import Simulation

from analysis.homogeneous.analysis import print_res, convert_to_reward, calculate_expected_reward, plt_graph

def run_experiment(sim_params, controller, controller_params):
    random.seed(sim_params["seed"])
    np.random.seed(sim_params["seed"])
    result_wait_t = []
    result_idle_t = []
    sim = Simulation(
            sim_params["num_floors"],
            sim_params["num_elevators"],
            sim_params["total_arrival_rate"],
            group_controller=controller, 
            controller_args=controller_params)

    print(f"\nSTARTING SIMULATION\n")
    start_time = time.time()

    simulation_data = list(sim.simulate(sim_params["simulation_duration"]))
    print("Simulation done for", sim.building.groupController)

    end_time = time.time()
    print(f"ENDING SIMULATION\n")
    print(f"EXECUTION TIME: {end_time - start_time:6.2f}s\n")
    print("Total Number of Cycles:", len(simulation_data))

    return simulation_data

def run_analysis(sim_params, simulation_data, label):
    num_floors = sim_params["num_floors"]
    num_elevators = sim_params["num_elevators"]

    print("ANALYZING")
    cycle_len_arr, reward_dict = convert_to_reward(simulation_data, num_floors, num_elevators)

    result_wait_t = []
    result_num_pass = []
    result_idle_t = []

    for floor, rewards in reward_dict["wait_time"].items():
        num_passengers = reward_dict["num_passenger"][floor]
        result = calculate_expected_reward(num_passengers, rewards)
        result["floor"] = floor
        result_wait_t.append(result)

    wait_time_data = pd.DataFrame(result_wait_t)

    for floor, rewards in reward_dict["num_passenger"].items():
        result = calculate_expected_reward(cycle_len_arr, rewards)
        result["floor"] = floor
        result_num_pass.append(result)

    passenger_arrival_data = pd.DataFrame(result_num_pass)

    for elevator_id, rewards in reward_dict["idle_time"].items():
        result = calculate_expected_reward(cycle_len_arr, rewards)
        result["elevator"] = elevator_id
        result_idle_t.append(result)

    idle_time_data = pd.DataFrame(result_idle_t)

    results = {
            "label": label,
            "wait_time": wait_time_data,
            "idle_time": idle_time_data,
            "passenger_arrival": passenger_arrival_data
            }
    return results

def run_comparison(*args):
    pass