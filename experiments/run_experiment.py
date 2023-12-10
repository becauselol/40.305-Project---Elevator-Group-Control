def run_experiment(sim_params, controller, controller_params):
    sim = Simulation(**sim_params, controller=controller, controller_params)

    print(f"\nSTARTING SIMULATION\n")
    start_time = time.time()

    simulation_data = list(sim.simulate(sim_params["simulation_duration"]))
    print("Simulation done for", sim.building.groupController)

    end_time = time.time()
    print(f"ENDING SIMULATION\n")
    print(f"EXECUTION TIME: {end_time - start_time:6.2f}s\n")
    print("Total Number of Cycles:", len(simulation_data))

    print("ANALYZING")
    cycle_len_arr, reward_dict = convert_to_reward(simulation_data, num_floors, num_elevators)
