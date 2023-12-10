from scipy.stats import binom
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import math
from collections import defaultdict 
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

        
def convert_to_reward(simulation_data, num_floors, num_elevators):
    """simulation_data is an array of dataframes"""
    
    cycles = []
    rewards = {}

    wait_time = []
    num_passenger = []


    wait_times = defaultdict(list)
    num_passengers = defaultdict(list)


    idle_times = defaultdict(list)
    idle_time_1 = []
    idle_time_2 = []


    for idx, cycle_data in enumerate(simulation_data):
        cycles.append(cycle_data.cycle_duration) # cycle duration
        
        # wait times per cycle
        wait_by_floor = cycle_data.passengers.groupby(['source']).sum()
        zeroes1 = pd.DataFrame(0, index = range(1,num_floors+1), columns = wait_by_floor.columns).astype(float)
        zeroes1.loc[wait_by_floor.index, wait_by_floor.columns] = wait_by_floor
        wait_w_zeroes = zeroes1
        wait_time.append(wait_w_zeroes['wait_time'])

        
        # number of passengers per cycle
        num_passenger_per_floor = cycle_data.passengers.groupby(['source']).count()
        zeroes2 = pd.DataFrame(0, index = range(1,num_floors+1), columns = num_passenger_per_floor.columns).astype(float)
        zeroes2.loc[num_passenger_per_floor.index, num_passenger_per_floor.columns] = num_passenger_per_floor
        num_w_zeroes = zeroes2
        num_passenger.append(num_w_zeroes['wait_time'])

        # finding idle time of each cycle for elevator 1
        for elevator_id in range(1, num_elevators + 1):

            end_idle = cycle_data.elevator_state['end_time'].loc[(cycle_data.elevator_state['state'] == Move.IDLE) & (cycle_data.elevator_state['elevator_id'] == elevator_id)]
            start_idle = cycle_data.elevator_state['start_time'].loc[(cycle_data.elevator_state['state'] == Move.IDLE) & (cycle_data.elevator_state['elevator_id'] == elevator_id)]
            idle = end_idle - start_idle
            idle_times[elevator_id].append(idle.sum())


    # add cycle values into a consolidated dictionary for each floor
    for cycle in num_passenger:
        for floor in cycle.index:
            num_passengers[floor].append(cycle.loc[floor])
    
    for cycle in wait_time:
        for floor in cycle.index:
            wait_times[floor].append(cycle.loc[floor])

    

    rewards['wait_time'] = wait_times
    rewards['num_passenger'] = num_passengers
    rewards["idle_time"] = idle_times

    # print(rewards)

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

def overall_stat(idle_time, wait_time):
    overall_uti = 1- (idle_time.loc[:, 'expected reward'].sum())/(idle_time.loc[:,'expected cycle length'].sum())
    overall_wait = (wait_time.loc[:, 'expected reward'].sum())/(wait_time.loc[:,'expected cycle length'].sum())

    print(f"""Overall Analysis:
Utilisation : {overall_uti: .6f}
Wait Time: {overall_wait: .6f}
    """)


# #plot scatter plot of wait time and idle time across different floors and elevators 
def plt_graph(data, graph_name, y_lim=(None, None)):
    
    if graph_name == "wait_time":
        x_col = 'floor'
    else:
        x_col = 'elevator'

    x = data.loc[:,x_col]
    y = data.loc[:,"steady state average"]
    
    y_errormin = data.loc[:, "interval 1-side length"]
    y_errormax = data.loc[:,"interval 1-side length"]
    
    y_error =[y_errormin, y_errormax]
    
    # plotting graph
    fig = plt.figure()
    plt.errorbar(x, y, yerr = y_error, fmt ='o')

    plt.xlabel('{} number'.format(x_col))
    plt.ylabel(graph_name)
    plt.ylim(*y_lim)

    #save graph as image
    img_path = "Results/{}.png".format(graph_name)
    fig.savefig(img_path)

def  plt_comparison(data):

    wait_t = data.loc[:, 'steady state average'].to_list()
    wait_t = [[v] for v in wait_t]
    x = data.loc[:, 'floor' ].to_list()
    fig = go.Figure()

    fig.add_trace(go.Box(y=wait_t, x=x, boxpoints=False, name = "simulation 1", marker_color='#FF4136')) # color="simulation_type"))

    
    fig.update_traces(
                    # x = x,
                    q1 = data.loc[:,'steady state average'].to_list(), 
                    q3 = data.loc[:,'steady state average'].to_list(), 
                    median = data.loc[:,'steady state average'].to_list(), 
                    sd = [0]*6,
                    lowerfence=data.loc[:, 'lower interval'].to_list(),
                    upperfence=data.loc[:, 'upper interval'].to_list(), 
                    mean=data.loc[:,'steady state average'].to_list(),
                    # line_width = 0.1,
                    selector = ({'name': 'simulation 1'}) )
    
    fig.add_trace(go.Box(y=wait_t , x =x,boxpoints=False, name = "simulation 2", marker_color='#FF851B')) # color="simulation_type"))

    fig.update_traces(
                    # x = x,
                    q1 = data.loc[:,'steady state average'].to_list(), 
                    q3 = data.loc[:,'steady state average'].to_list(), 
                    median = data.loc[:,'steady state average'].to_list(), 
                    sd = [0]*6,
                    lowerfence=data.loc[:, 'lower interval'].to_list(),
                    upperfence=data.loc[:, 'upper interval'].to_list(), 
                    mean=data.loc[:,'steady state average'].to_list(),
                    # line_width = 0.1,
                    selector = ({'name': 'simulation 2'}) )
    

    fig.update_layout(
    yaxis_title='Wait Time',
    boxmode='group' # group together boxes of the different traces for each value of x
    )
    
    #save graph as image
    img_path = "Results/{}.png".format('comparison_graph')
    fig.write_image(img_path)



