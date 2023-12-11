import os
from tqdm import tqdm
import pandas as pd

from analysis.run_experiment import run_experiment, run_analysis
import simulation.classes.groupController as gControl
import simulation.classes.arrival_pattern as arrPattern
from simulation.utils import get_all_idle_combinations

from analysis.utils import print_res, convert_to_reward, calculate_expected_reward, plt_graph, overall_stat, plt_comparison

if __name__ == "__main__":

    # Seed for randomness
    """
    Users can manipulate this section of the code to test various policies
    """
    params = {
            "seed": 1,
            "num_floors": 6,
            "num_elevators": 3,
            "simulation_duration": 72000
            }

    # Select the policy u want to choose
    """
    Controller Policies can be set to
    - Random
    - Zoning
    - Nearest
    """
    chosen_policy = "Nearest"

    """
    Arrival Pattern can be set to
    - Uniform
    - Ground Heavy
    """
    chosen_arrival_pattern = "Ground Heavy"

    """
    For Idle Floor configurations
    Make sure the length of the array is equal to the number of elevators
    And check that each value is between the floors 1 to the number of floors
    """
    idle_floor_configuration = [3, 3, 3]

    assert len(idle_floor_configuration) == params["num_elevators"]
    for v in idle_floor_configuraion:
        assert 1 <= v <= params["num_floors"]

    output_folder = f"Results/data/simulation_{chosen_policy}_{chosen_arrival_pattern}_{'_'.join([str(i) for i in idle_floor_configuration])}"
    
    print("random seed:", params["seed"])
    print("simulation duration:", params["simulation_duration"])
    print("number of floors:", params["num_floors"])
    print("number of elevators:", params["num_elevators"])

    """
    The following parameters are as detailed in the experiments
    They are the default settings
    """
    uniform_arrival_args = {
            "num_floors": params["num_floors"],
            "total_arrival_rate": 0.6
            }

    ground_heavy_args = {
            "num_floors": params["num_floors"],
            "total_arrival_rate": 0.6,
            "ground_percentage": 0.35
            }

    arrival_patterns = {
            "Ground Heavy": (arrPattern.GroundHeavy, ground_heavy_args),
            "Uniform": (arrPattern.UniformArrival, uniform_arrival_args)
            }

    zoning_params = {
            "zones": {
                    1: [1, 2],
                    2: [3, 4],
                    3: [5, 6]
                }
            }
    controller_policies = {
            "Random": (gControl.RandomController, {}),
            "Zoning": (gControl.ZoningController, zoning_params),
            "Nearest": (gControl.NearestElevatorController, {})
            }

    arrival_pattern_class, arrival_args = arrival_patterns[chosen_arrival_pattern]
    controller_class, controller_params = controller_policies[chosen_policy]
    controller_params["idle_floors"] = idle_floor_configuration 
    
    sim_result = run_experiment(params, arrival_pattern_class, arrival_args, controller_class, controller_params)

    result = run_analysis(params, sim_result, chosen_policy) 
    result["overall_stats"] = result["overall_stats"].set_index("stat label")

    trial_result = {
            "controller": chosen_policy,
            "idle_floor_config": tuple(idle_floor_configuration),
            "num_cycles": result["num_cycles"],
            "wait_time":result["overall_stats"].loc["avg_wait_time", "steady state average"],
            "wait_time_interval":result["overall_stats"].loc["avg_wait_time", "interval 1-side length"],
            "idle_time":result["overall_stats"].loc["avg_idle_time", "steady state average"],
            "idle_time_interval":result["overall_stats"].loc["avg_idle_time", "interval 1-side length"]
            }

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pd.DataFrame([trial_result]).to_csv(f"{output_folder}/overall_stats.tsv", sep="\t", index=False)
    result["wait_time"].to_csv(f"{output_folder}/wait_time_data.tsv", sep="\t", index=False)
    result["passenger_arrival"].to_csv(f"{output_folder}/passenger_arrival_data.tsv", sep="\t", index=False)
    result["idle_time"].to_csv(f"{output_folder}/idle_time_data.tsv", sep="\t", index=False)
