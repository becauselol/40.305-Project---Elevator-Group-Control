from scipy.stats import binom
from scipy import stats
import numpy as np
import random
from simulation.classes.sim import Simulation
from simulation.classes.controller import Move


def homogeneous_analysis():
    random.seed(1)
    np.random.seed(1)
    num_floors = 4
    simulation_duration = 24 * 60 * 5
    sim = Simulation(num_floors)

    
    for idx, cycle_data in enumerate(sim.simulate(simulation_duration)):
        print("cycle:", idx)
        print("cycle duration:", cycle_data.cycle_duration)
        print(cycle_data.passengers.head())

        
def convert_to_reward(simulation_data):
    """simulation_data is an array of dataframes"""
    
    cycles = []
    rewards = {}

    wait_time = []
    num_passenger = []
    idle_time_1 = []
    idle_time_2 = []


    for idx, cycle_data in enumerate(simulation_data):
        cycles.append(cycle_data.cycle_duration)
        wait_time.append(cycle_data.passengers['wait_time'].sum())
        num_passenger.append(len(cycle_data.passengers))

        # finding idle time of each cycle for elevator 1
        end_idle_1 = cycle_data.elevator_state['end_time'].loc[(cycle_data.elevator_state['state'] == Move.IDLE) & (cycle_data.elevator_state['elevator_id'] == 1)]
        start_idle_1 = cycle_data.elevator_state['start_time'].loc[(cycle_data.elevator_state['state'] == Move.IDLE) & (cycle_data.elevator_state['elevator_id'] == 1)]
        idle_1 = end_idle_1 - start_idle_1
        idle_time_1.append(idle_1.sum())

        # finding idle time of each cycle for elevator 2
        end_idle_2 = cycle_data.elevator_state['end_time'].loc[(cycle_data.elevator_state['state'] == Move.IDLE) & (cycle_data.elevator_state['elevator_id'] == 2)]
        start_idle_2 = cycle_data.elevator_state['start_time'].loc[(cycle_data.elevator_state['state'] == Move.IDLE) & (cycle_data.elevator_state['elevator_id'] == 2)]
        idle_2 = end_idle_2 - start_idle_2
        idle_time_2.append(idle_2.sum())




    rewards['wait_time'] = wait_time
    rewards['num_passenger'] = num_passenger 
    rewards['idle_time_1'] = idle_time_1
    rewards['idle_time_2'] = idle_time_2

    
    return cycles, rewards

def calculate_expected_reward(C, R, alpha=0.05):
    """Takes in 2 arrays and a level of significance alpha
Arrays are C and R that need to be of equal length
    
    """
    assert len(C) == len(R)

    n = len(C)
    result = {}
    result["expected reward"] = np.mean(R)
    result["expected cycle length"] = np.mean(C)
    
    # expectation estimate
    result["steady state average"] = result["expected reward"] / result["expected cycle length"]
    

    
    # variance estimate
    result["np cov"] =  np.cov(R, C)
    result["reward variance"] = result["np cov"][0][0]
    result["cycle variance"] = result["np cov"][1][1]
    
    result["covariance estimate"] = np.cov(R, C)[1][0]
    
    result["sample variance"] = \
        result["reward variance"] \
        - 2*(result["steady state average"])*result["covariance estimate"] \
        + (result["steady state average"]**2)*result["cycle variance"]
    
    # confidence interval
    result["interval 1-side length"] = \
        (np.sqrt(result["sample variance"]) * (-stats.norm.ppf(alpha/2))) / \
        (result["expected cycle length"] * np.sqrt(n))
    
    result["upper interval"] = result["steady state average"] + result["interval 1-side length"]
    result["lower interval"] = result["steady state average"] - result["interval 1-side length"]
    
    
    return result


def print_res(result, variable_name = ""):
    print(f"""---
Results : {variable_name}
---
Expectation Estimate: {result["steady state average"]:.6f}
Variance Estimate   : {result["sample variance"]:.6f}
Confidence Interval : [{result["lower interval"]:.6f}, {result["upper interval"]:.6f}]
    
    """)
