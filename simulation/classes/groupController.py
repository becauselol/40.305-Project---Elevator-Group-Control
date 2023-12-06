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
        self.liftControllers = {i: LiftController(i, self.num_floors) for i in range(1, num_elevators + 1)}
        if idle_floors:
            self.idle_floors = idle_floors
        else:
            # defaults to all being level 1
            self.idle_floors = [1] * num_elevators

        self.alternate = True

    def add_ext_call(self, floor_call, direction, time):
        if direction == Move.UP:
            if self.ext_call[floor_call - 1].up_call:
                return False
            self.ext_call[floor_call - 1].set_up_call(time)
        elif direction == Move.DOWN:
            if self.ext_call[floor_call - 1].down_call:
                return False
            self.ext_call[floor_call - 1].set_down_call(time)
        return True

    def consume_ext_call(self, floor, move_direction):
        if move_direction == Move.UP:
            self.ext_call[floor - 1].up_call = False
            self.ext_call[floor - 1].up_call_time = float("inf")
        elif move_direction == Move.DOWN:
            self.ext_call[floor - 1].down_call = False
            self.ext_call[floor - 1].down_call_time = float("inf")

    def request_is_empty(self):
        return self.liftController[1].request_is_empty()

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
        # Everything is assigned to the first one, should be correct
        self.alternate = not self.alternate
        return 1 if self.alternate else 2
        # return 1

    def add_ext_call_to_lift(self, lift_id, floor_call, direction, time):
        self.liftControllers[lift_id].add_ext_call(floor_call, direction, time)
