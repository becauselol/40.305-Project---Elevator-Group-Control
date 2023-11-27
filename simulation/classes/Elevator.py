from queue import PriorityQueue
from enum import Enum

class Move(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0



class Elevator:

    def __init__(self, capacity, floors, move_speed = 1, start_floor = 1):
        self.capacity = capacity
        self.floors = floors
        self.move_speed = move_speed
        self.current_floor = start_floor
        self.direction = Move.IDLE
        self.wait_time = 0.5
        self.wait_idle_time = 2

        self.alighting_people = [[] for _ in range(floors)]

    def move_up(self):
        if self.current_floor + 1 > self.floors:
            raise Exception("Max floor reached")

        self.current_floor += 1

    def move_down(self):
        if self.current_floor - 1 < 1:
            raise Exception("Lowest floor reached")
        
        self.current_floor -= 1

    def move_down_n(self, n):
        for _ in range(n):
            self.move_down()

    def move_up_n(self, n):
        for _ in range(n):
            self.move_up()

    def get_num_passengers(self):
        return sum([len(arr) for arr in self.alighting_people])

    def add_passenger(self, passenger):
        self.alighting_people[passenger.dest - 1].append(passenger)

class ExtCall:
    def __init__(self, floor):
        self.floor = floor
        self.up_call = False
        self.down_call = False
        self.up_call_time = -1
        self.down_call_time = -1

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

    def no_call(self):
        return not self.up_call and not self.down_call


class ElevatorController:

    def __init__(self, num_floors):
        # Maintain 3 things
        # Number to pick up
        # Up pq, Dwon pq
        # Then just subtract the number to pick up as you go along
        # up calls
        self.idle_floor = 1

        self.ext_call = [ExtCall(i) for i in range(1, num_floors + 1)]

        # These are the internal calls
        self.int_call = PriorityQueue()


    def add_ext_call(self, time, elevator, floor_call, direction):
        if direction == Move.UP:
            self.ext_call[floor_call - 1].set_up_call(time)
        elif direction == Move.DOWN:
            self.ext_call[floor_call - 1].set_down_call(time)


    def add_int_call(self, time, elevator, floor_call):
        self.int_call.put(floor_call * elevator.direction.value)

    def request_is_empty(self):
        return len(self.int_call.queue) == 0 and all([e_call.no_call() for e_call in self.ext_call])

    def check_next_move(self, time, elevator, event):
        """
        Return the parameters of the next move that the elevator is supposed to do
        """
        # Check if the queues are empty
        if self.request_is_empty():
            return -1

        # If elevator is moving along a certain direction, check what the next move is supposed to be
        # If elevator is on up progress
        if elevator.direction == Move.UP:
            min_floor = "inf"
            if not self.int_call.empty():
                min_floor = min(min_floor, self.int_call.queue[0][0])

            for index in range(elevator.current_floor, len(self.ext_call)):
                e_call = self.ext_call[index]
                if e_call.up_call:
                    min_floor = min(min_floor, e_call.floor)
                    break

            if min_floor != "inf":
                # We have found the next floor to go to
                return min_floor
                # Time to change direction

            elevator.direction = Move.DOWN
            # Now the max_floor is the next_floor to go to
            for index in range(elevator.current_floor - 1, -1, -1):
                if self.ext_call[index].down_call:
                    return self.ext_call[index].floor

        elif elevator.direction == Move.DOWN:
            max_floor = "-inf"
            if not self.int_call.empty():
                max_floor = max(max_floor, -1 * self.int_call.queue[0][0])

            for index in range(elevator.current_floor - 2, -1, -1):
                e_call = self.ext_call[index]
                if e_call.down_call:
                    max_floor = max(max_floor, e_call.floor)
                    break

            if max_floor != "-inf":
                return max_floor

            elevator.direction = Move.UP

            for index in range(elevator.current_floor, len(self.ext_call)):
                e_call = self.ext_call[index]
                if e_call.up_call:
                    return e_call.floor


    def get_new_call(self, time, elevator, event):
        """
        Check what the new call is and respond accordingly
        """
        pass

    def interrupt_move(self, time, elevator, reachFloorEvent):
        """
        Figure out what is the update required to the reachFloorEvent
        and return the updated reachFloorEvent parameters
        """
        pass

    def get_idle_floor(self, elevator):
        """
        Eventually controller will access elevators to determine
        Which IDLE direction
        """
        return self.idle_floor

    def move_idle_direction(self, elevator):
        return Move.UP.value if elevator.current_floor < self.idle_floor else Move.DOWN.value

