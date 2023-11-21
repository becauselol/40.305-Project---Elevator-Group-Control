from .Elevator import Elevator
from .Controller import RoundRobinAlgorithm

class Building:
    
    def __init__(self, num_elevators, num_floors, elevator_capacity):
        self.num_elevators = num_elevators
        self.num_floors = num_floors
        self.elevators = [Elevator(elevator_capacity, num_floors)] * num_elevators
