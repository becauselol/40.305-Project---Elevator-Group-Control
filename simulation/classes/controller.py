from abc import ABC, abstractmethod
from heapq import heappush, heappop
from enum import Enum

from . import elevator 

class Move(Enum):
    UP = 1
    DOWN = -1
    NONE = 0

class ExtCall:
    def __init__(self, floor):
        self.floor = floor
        self.up_call = False
        self.down_call = False
        self.up_call_time = float("inf")
        self.down_call_time = float("inf")

    def set_up_call(self, time):
        if self.up_call:
            return
        
        self.up_call = True
        self.up_call_time = time

    def set_down_call(self, time):
        if self.down_call:
            return
        
        self.down_call = True
        self.down_call_time = time

    def has_call(self):
        return self.up_call or self.down_call

    def no_call(self):
        return not self.up_call and not self.down_call

    def min_call(self):
        if self.up_call_time < self.down_call_time:
            return self.up_call_time 
        else:
            return self.down_call_time

class Controller(ABC):

    @abstractmethod
    def where_next_moving(self):
        pass

    @abstractmethod
    def where_next_stationary(self):
        pass

class LiftController(Controller):
    def __init__(self, id, num_floors, idle_floor=1):
        self.id = id
        self.name = "Lift Controller"
        self.idle_floor = idle_floor
        self.num_floors = num_floors
        self.elevator = elevator.Elevator(self.id, self.num_floors)

        # This is now an assigned external call
        self.ext_call = [ExtCall(i) for i in range(1, num_floors + 1)]

        # These are the internal calls
        self.int_call = []

    def add_ext_call(self, floor_call, direction, time):
        if direction == Move.UP:
            self.ext_call[floor_call - 1].set_up_call(time)
        elif direction == Move.DOWN:
            self.ext_call[floor_call - 1].set_down_call(time)

    def add_int_call(self, floor_call, direction):
        if floor_call * direction.value not in self.int_call:
            heappush(self.int_call, floor_call * direction.value)

    def request_is_empty(self):
        return len(self.int_call) == 0 and all([e_call.no_call() for e_call in self.ext_call])

    def consume_ext_call(self, floor, move_direction):
        if move_direction == Move.UP:
            self.ext_call[floor - 1].up_call = False
            self.ext_call[floor - 1].up_call_time = float("inf")
        elif move_direction == Move.DOWN:
            self.ext_call[floor - 1].down_call = False
            self.ext_call[floor - 1].down_call_time = float("inf")

    def consume_int_call(self, floor, move_direction):
        if self.int_call and self.int_call[0] == floor * move_direction.value:
            heappop(self.int_call)

    def time_to_idle_floor(self, elevator):
        return abs(elevator.floor - self.get_idle_floor(elevator)) * elevator.move_speed

    def get_idle_floor(self, elevator):
        return self.idle_floor

    def at_idle(self, elevator):
        return self.idle_floor == elevator.floor

    def get_next_floor(self, floor, move_direction):
        if move_direction == Move.UP:
            # Let's check for the nearest up call
            nearest_up = set([e_call.floor for e_call in self.ext_call if e_call.up_call and e_call.floor >= floor])
            if self.int_call:
                nearest_up.add(self.int_call[0])

            if nearest_up:
                return min(nearest_up)

            # There is no up call, let's check for the farthest down call
            farthest_down = set([e_call.floor for e_call in self.ext_call if e_call.down_call and e_call.floor >= floor])
            if farthest_down:
                return max(farthest_down)

        elif move_direction == Move.DOWN:
            nearest_down = set([e_call.floor for e_call in self.ext_call if e_call.down_call and e_call.floor <= floor])
            if self.int_call:
                nearest_down.add(move_direction.value * self.int_call[0])

            if nearest_down:
                return max(nearest_down)

            # There is no up call, let's check for the farthest down call
            farthest_up = set([e_call.floor for e_call in self.ext_call if e_call.up_call and e_call.floor <= floor])
            if farthest_up:
                return min(farthest_up)

        print(move_direction)
        print("elevator floor:", floor)
        print("elevator_id:", self.id)
        print("int call:", self.int_call)
        print("ext up call:", [e_call.up_call for e_call in self.ext_call])
        print("ext down call:", [e_call.down_call for e_call in self.ext_call])
        
        raise Exception("No remaining calls in selected direction")



    def where_next_moving(self, elevator_floor, move_direction):
        """
        Returns the next Floor
        """
        return self.get_next_floor(elevator_floor, move_direction)



    def where_next_stationary(self, elevator_floor, move_direction):
        """
        Returns the next direction
        """
        # Any internal calls left?
        # print("int call:", self.int_call)
        # print("ext up call:", [e_call.up_call for e_call in self.ext_call])
        # print("ext down call:", [e_call.down_call for e_call in self.ext_call])
        if self.int_call:
            # if yes continue same direction
            return move_direction

        # any calls on this floor and above that go in same direction?
        if move_direction == Move.UP:
            above_calls = [e_call.floor for e_call in self.ext_call if e_call.has_call() and e_call.floor > elevator_floor]

            if self.ext_call[elevator_floor - 1].up_call:
                above_calls.append(elevator_floor)

            if above_calls:
                return move_direction

            down_calls = [e_call.floor for e_call in self.ext_call if e_call.has_call() and e_call.floor < elevator_floor]

            if self.ext_call[elevator_floor - 1].down_call:
                down_calls.append(elevator_floor)
            if down_calls:
                return Move.DOWN
        
        elif move_direction == Move.DOWN:
            down_calls = [e_call.floor for e_call in self.ext_call if e_call.has_call() and e_call.floor < elevator_floor]

            if self.ext_call[elevator_floor - 1].down_call:
                down_calls.append(elevator_floor)

            if down_calls:
                return move_direction

            above_calls = [e_call.floor for e_call in self.ext_call if e_call.has_call() and e_call.floor > elevator_floor]

            if self.ext_call[elevator_floor - 1].up_call:
                above_calls.append(elevator_floor)

            if above_calls:
                return Move.UP

        return Move.WAIT

    def check_direction(self, elevator_floor):
        # based on the current floor
        # check which external call happened first

        # compare on 3 factors
        # 1: which call is the earliest
        # 2: which floor is the closest
        # 3: finally, just prefers lower floors
        min_times = [(e_call.min_call(), abs(elevator_floor - e_call.floor), e_call.floor) for e_call in self.ext_call if e_call.has_call()]
        call_time, dist_floor, target_floor = min(min_times)

        if target_floor == elevator_floor:
            # check whether its an up or down call
            e_call = self.ext_call[target_floor - 1]
            if call_time == e_call.up_call_time:
                return Move.UP
            else:
                return Move.DOWN

        # if the target floor is not the current floor
        if target_floor > elevator_floor:
            return Move.UP
        else:
            return Move.DOWN



