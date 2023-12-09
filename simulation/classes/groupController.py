import random
from enum import Enum
from abc import ABC, abstractmethod
from .controller import ExtCall, LiftController
from .elevator import Elevator

class State(Enum):
    IDLE = 0
    MOVING = 1

class GroupController(ABC):
    def __init__(self, num_floors, num_elevators, idle_floors=None):
        self.name = "Group Controller"
        self.num_floors = num_floors
        self.num_elevators = num_elevators

        if idle_floors:
            self.idle_floors = idle_floors
        else:
            # defaults to all being level 1
            self.idle_floors = [1] * num_elevators

        self.liftControllers = {i: LiftController(i, self.num_floors, self.idle_floors[i - 1]) for i in range(1, num_elevators + 1)}


    @abstractmethod
    def assign_call(self, floor_call, direction, time):
        """
        Assigns the new external call to a specific liftController

        Once a new external call is assigned to a LiftController
        The new external call is then consumed by the group controller
        
        To help with this We want the following
        - Position of elevators
        - Direction of each elevator
            - We need to have direction, state and floor
        - Capacity in each elevator
        - The calls registered for each elevator
        """
        pass

    def add_ext_call_to_lift(self, lift_id, floor_call, direction, time):
        self.liftControllers[lift_id].add_ext_call(floor_call, direction, time)

class RandomController(GroupController):
    def __init__(self, num_floors, num_elevators, idle_floors=None):
        super().__init__(num_floors, num_elevators, idle_floors)
        self.name = "Random Assignment"
    
    def assign_call(self, floor_call, direction, time):
        return random.randint(1, self.num_elevators)

class ZoningController(GroupController):
    def __init__(self, num_floors, num_elevators, idle_floors=None, zones=None):
        """
        Zones should be an dictionary containing the floors each elevator is assigned to
        floors assigned in the dictionary should be in the form of an iterable
        if multiple elevators are assigned to each floor, random choice is done for assignment
        """
        super().__init__(num_floors, num_elevators, idle_floors)
        self.name = "Random Assignment"
        # Check for each floors assigned elevator
        self.elevator_to_floor = zones
        self.floor_to_elevator = defaultdict(list)

        for elevator_id, floors in self.elevator_to_floor.items():
            for floor in floors:
                self.floor_to_elevator[floor].append(elevator_id)
    
    def assign_call(self, floor_call, direction, time):
        return random.choice(self.floor_to_elevator[floor])

