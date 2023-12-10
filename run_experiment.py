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

    start_time = time.time()

    simulation_data = list(sim.simulate(sim_params["simulation_duration"]))

    end_time = time.time()

    return simulation_data

def run_analysis(sim_params, simulation_data, label):
    num_floors = sim_params["num_floors"]
    num_elevators = sim_params["num_elevators"]

    cycle_len_arr, reward_dict = convert_to_reward(simulation_data, num_floors, num_elevators)

    result_wait_t = []
    result_num_pass = []
    result_idle_t = []

    overall_stat_calculation = dict(
            avg_wait_time=("num_passenger", "wait_time"),
            passenger_arrival_rate=("cycle_duration", "num_passenger"),
            avg_idle_time=("cycle_duration", "idle_time")
            )

    overall_stat_arr = []
    for stat_label, (cycle, reward) in overall_stat_calculation.items():
        result = calculate_expected_reward(reward_dict["overall"][cycle], reward_dict["overall"][reward])
        result["reward label"] = reward
        result["cycle label"] = cycle
        result["stat label"] = stat_label
        overall_stat_arr.append(result)

    overall_stat_data = pd.DataFrame(overall_stat_arr)

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
            "passenger_arrival": passenger_arrival_data,
            "overall_stats": overall_stat_data,
            "num_cycles": len(cycle_len_arr)
            }
    return results

def run_comparison(*args):
    pass
