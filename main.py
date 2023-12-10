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

    sim_result_random = run_experiemnt(params, RandomController)
    sim_result_zoning = run_experiemnt(params, ZoningController, zoning_params)
    sim_result_nearest = run_experiemnt(params, NearestElevatorController)

    result_random = run_analysis(sim_result_random, "Random") 
    result_zoning = run_analysis(sim_result_zoning, "Zoning")
    result_nearest = run_analysis(sim_result_nearest, "Nearest")
