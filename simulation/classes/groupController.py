from enum import Enum
from .controller import ExtCall, LiftController
from .elevator import Elevator

class State(Enum):
    IDLE = 0
    MOVING = 1

class GroupController:
    def __init__(self, num_floors, num_elevators, idle_floors=None):
        self.name = "Group Controller"
        self.state = State.IDLE
        self.num_floors = num_floors
        self.ext_call = [ExtCall(i) for i in range(1, num_floors + 1)]
        self.liftController = [LiftController(self.num_floors)] * num_elevators
        if idle_floors:
            self.idle_floors = idle_floors
        else:
            # defaults to all being level 1
            self.idle_floors = [1] * num_elevators

    def add_ext_call(self, floor_call, direction, time):
        if direction == Move.UP:
            self.ext_call[floor_call - 1].set_up_call(time)
        elif direction == Move.DOWN:
            self.ext_call[floor_call - 1].set_down_call(time)

    def consume_ext_call(self, floor, move_direction):
        if move_direction == Move.UP:
            self.ext_call[floor - 1].up_call = False
            self.ext_call[floor - 1].up_call_time = float("inf")
        elif move_direction == Move.DOWN:
            self.ext_call[floor - 1].down_call = False
            self.ext_call[floor - 1].down_call_time = float("inf")

    def request_is_empty(self):
        pass

    def respond_new_ext_call(self):
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
