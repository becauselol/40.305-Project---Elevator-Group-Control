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

    def __init__(self):
        # up calls
        self.up = PriorityQueue()
        self.next_up = PriorityQueue()

        # each call can either be interior or exterior
        # down calls
        self.down = PriorityQueue()
        self.next_down = PriorityQueue()

        self.idle_floor = 1


    def add_floor(self, elevator: Elevator, floor_call, ext):
        # ext is either True or False to indicate whether it is exterior or interiro
        if floor_call < elevator.current_floor:
            self.down.put((floor_call, ext))
        elif floor_call > elevator.current_floor:
            self.up.put((floor_call, ext))

    def next_floor(self, elevator: Elevator):
        if elevator.direction == Move.DOWN:
            return self.down.get()
        elif elevator.direction == Move.UP or elevator.direction == Move.IDLE:
            return self.up.get()

    def request_is_empty(self):
        return self.up.empty() and self.down.empty()

    def check_correct_move(self, time, elevator, event):
        # check if the movement can be interrupted
        # suppose elevator is moving up
        if elevator.direction == Move.UP:
            # is the elevator past the floor already?
            while time - event.prev_time > (self.up[0][0] - elevator.current_floor) * elevator.move_speed:
                self.next_up.put(self.up.get())
        

    def get_idle_floor(self, elevator):
        """
        Eventually controller will access elevators to determine
        Which IDLE direction
        """
        return self.idle_floor

    def move_idle_direction(self, elevator):
        return Move.UP if elevator.current_floor < self.idle_floor else Move.DOWN

