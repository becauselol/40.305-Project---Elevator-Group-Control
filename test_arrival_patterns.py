from simulation.classes.arrival_pattern import ArrivalPattern, UniformArrival, GroundHeavy

if __name__ == "__main__":
    arrival_pattern = GroundHeavy(6, 1, 0.35)
    rate_matrix = arrival_pattern.get_rate_matrix()
    for arr in rate_matrix:
        print(arr)
