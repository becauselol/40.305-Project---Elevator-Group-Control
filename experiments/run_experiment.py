def run_experiment(sim_params, controller, controller_params):
    result_wait_t = []
    result_idle_t = []
    sim = Simulation(**sim_params, controller=controller, controller_params)

    print(f"\nSTARTING SIMULATION\n")
    start_time = time.time()

    simulation_data = list(sim.simulate(sim_params["simulation_duration"]))
    print("Simulation done for", sim.building.groupController)

    end_time = time.time()
    print(f"ENDING SIMULATION\n")
    print(f"EXECUTION TIME: {end_time - start_time:6.2f}s\n")
    print("Total Number of Cycles:", len(simulation_data))

    return simulation_data

def run_analysis(simulation_data, name):
    print("ANALYZING")
    cycle_len_arr, reward_dict = convert_to_reward(simulation_data, num_floors, num_elevators)

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

    results = {
            "name": name
            "wait_time", wait_time_data,
            "idle_time": idle_time_data
            }
    return results

def run_comparison(*args)
