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

class ElevatorController:

    def __init__(self, num_floors):
        # Maintain 3 things
        # Number to pick up
        # Up pq, Dwon pq
        # Then just subtract the number to pick up as you go along
        # up calls
        self.idle_floor = 1

        self.ext_up = [(False, 0)] * num_floors
        self.ext_down = [(False, 0)] * num_floors
        self.up = PriorityQueue()
        self.next_up = PriorityQueue()

        # each call can either be interior or exterior
        # down calls
        self.down = PriorityQueue()
        self.next_down = PriorityQueue()


    def add_ext_call(self, time, elevator, floor_call, direction):
        pass

    def add_int_call(self, time, elevator, floor_call):
        pass

    def add_floor(self, elevator: Elevator, floor_call, ext, time):
        pass

    def next_floor(self, elevator: Elevator):
        pass

    def request_is_empty(self):
        pass

    def check_next_move(self, time, elevator, event):
        """
        Return the parameters of the next move that the elevator is supposed to do
        """
        pass



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

