# HELPs recognize this as the main folder in the package

from analysis.homogeneous.analysis import homogeneous_analysis

if __name__ == "__main__":
    random.seed(1)
    np.random.seed(1)
    num_floors = 4
    simulation_duration = 24 * 60 * 5
    sim = Simulation(num_floors)

    
    for idx, cycle_data in enumerate(sim.simulate(simulation_duration)):
        print("cycle:", idx)
        print("cycle duration:", cycle_data.cycle_duration)
        print(cycle_data.passengers.head())

