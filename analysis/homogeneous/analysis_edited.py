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

        
def output_to_array(df):
    
    cycles = []
    rewards = {}
    wait_time = []
    no_passenger = []
    idle_t = []

    
    for idx, cycle_data in enumerate(df):
        cycles.append(cycle_data.cycle_duration)
        wait_time.append(cycle_data.passengers['wait_time'].sum())
        no_passenger.append(len(cycle_data.passengers))

        # finding idle time of each cycle
        end_idle = cycle_data.elevator_state['end_time'].loc[cycle_data.elevator_state['state'] == Move.IDLE]
        start_idle = cycle_data.elevator_state['start_time'].loc[cycle_data.elevator_state['state'] == Move.IDLE]
        idle = end_idle - start_idle
        idle_t.append(idle.sum())

    rewards['wait_t'] = wait_time
    rewards['num_passenger'] = no_passenger 
    rewards['idle_time'] = idle_t

    
    return [cycles, rewards]

def calculate_expected(C, R):
    alpha = 0.05 
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