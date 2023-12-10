from run_experiment import run_experiment, run_analysis
import simulation.classes.groupController as gControl

from analysis.homogeneous.analysis import print_res, convert_to_reward, calculate_expected_reward, plt_graph, overall_stat, plt_comparison

if __name__ == "__main__":
    print("RUNNING VARIOUS SIMULATIONS\n")

    print("RUNNING")
    # Seed for randomness
    params = {
            "seed": 1,
            "num_floors": 6,
            "num_elevators": 3,
            "total_arrival_rate": 0.6,
            "simulation_duration": 72000
            }
    
    print("random seed:", params["seed"])
    print("simulation duration:", params["simulation_duration"])
    print("number of floors:", params["num_floors"])
    print("number of elevators:", params["num_elevators"])
    
    controller_params = {
            "idle_floors": [1] * params["num_elevators"]
            }

    zoning_params = {
            "idle_floors": [1] * params["num_elevators"],
            "zones": {
                    1: [1, 2],
                    2: [3, 4],
                    3: [5, 6]
                }
            }

    sim_result_random = run_experiment(params, gControl.RandomController, controller_params)
    sim_result_zoning = run_experiment(params, gControl.ZoningController, zoning_params)
    sim_result_nearest = run_experiment(params, gControl.NearestElevatorController, controller_params)

    result_random = run_analysis(params, sim_result_random, "Random") 
    result_zoning = run_analysis(params, sim_result_zoning, "Zoning")
    result_nearest = run_analysis(params, sim_result_nearest, "Nearest")

    # We want comparison graph for the different policies
    # We also want to compare the different idle floor settings
    # We will then do a comparison
