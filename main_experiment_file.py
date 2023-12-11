from tqdm import tqdm
import pandas as pd

from run_experiment import run_experiment, run_analysis
import simulation.classes.groupController as gControl
import simulation.classes.arrival_pattern as arrPattern
from simulation.utils import get_all_idle_combinations


from analysis.homogeneous.analysis import print_res, convert_to_reward, calculate_expected_reward, plt_graph, overall_stat, plt_comparison

if __name__ == "__main__":
    print("RUNNING VARIOUS SIMULATIONS\n")

    print("RUNNING")
    # Seed for randomness
    params = {
            "seed": 1,
            "num_floors": 6,
            "num_elevators": 3,
            "simulation_duration": 72000
            }
    
    print("random seed:", params["seed"])
    print("simulation duration:", params["simulation_duration"])
    print("number of floors:", params["num_floors"])
    print("number of elevators:", params["num_elevators"])

    zoning_params = {
            "zones": {
                    1: [1, 2],
                    2: [3, 4],
                    3: [5, 6]
                }
            }

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
            "Uniform": ("all_data_uniform.tsv", arrPattern.UniformArrival, uniform_arrival_args),
            "Ground Heavy": ("all_data_groundheavy.tsv", arrPattern.GroundHeavy, ground_heavy_args)
            }

    conditions = {
            "Random": (gControl.RandomController, {}),
            "Zoning": (gControl.ZoningController, zoning_params),
            "Nearest": (gControl.NearestElevatorController, {})
            }
    
    all_idle_combinations = get_all_idle_combinations(params["num_floors"], params["num_elevators"])

    print("idle combination:", len(all_idle_combinations))

    for arrival_pattern_name, (output_file_name, arrival_pattern, arrival_args) in arrival_patterns.items():

        print("RUNNING for:", arrival_pattern_name, "arrival pattern")

        collated_result = []
    
        for idle_floor_combination in tqdm(all_idle_combinations):
            for controller_name, (controller_class, controller_params) in conditions.items():
                controller_params["idle_floors"] = idle_floor_combination
                sim_result = run_experiment(params, arrival_pattern, arrival_args, controller_class, controller_params)
        
                result = run_analysis(params, sim_result, controller_name) 
                result["overall_stats"] = result["overall_stats"].set_index("stat label")
        
                trial_result = {
                        "controller": controller_name,
                        "idle_floor_config": tuple(idle_floor_combination),
                        "num_cycles": result["num_cycles"],
                        "wait_time":result["overall_stats"].loc["avg_wait_time", "steady state average"],
                        "wait_time_interval":result["overall_stats"].loc["avg_wait_time", "interval 1-side length"],
                        "idle_time":result["overall_stats"].loc["avg_idle_time", "steady state average"],
                        "idle_time_interval":result["overall_stats"].loc["avg_idle_time", "interval 1-side length"]
                        }
                collated_result.append(trial_result)
    
    
        collated_df = pd.DataFrame(collated_result)
        collated_df.to_csv(output_file_name, sep="\t", index=False)
