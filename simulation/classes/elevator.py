from enum import Enum
from . import controller 

class State(Enum):
    MOVING = 1
    IDLE = 0
    WAIT = 2
    WAIT_UPDATE = 3
    MOVING_TO_IDLE = float("inf")




class Elevator:
    def __init__(self, id, num_floors, capacity=float("inf"), idle_floor=1):
        self.id = id
        self.num_floors = num_floors
        self.capacity = capacity
        self.direction = controller.Move.IDLE
        self.state = State.IDLE
        self.floor = idle_floor
        self.move_speed = 1
        self.wait_to_idle = 1
        self.open_door_time = 0.5

        self.alighting_people = [[] for _ in range(num_floors)]

    def add_passenger(self, passenger):
        self.alighting_people[passenger.dest - 1].append(passenger)

    def get_num_passengers(self):
        return sum(len(arr) for arr in self.alighting_people)

    def get_alighting(self, floor):
        return self.alighting_people[floor - 1]

    def check_alighting(self, floor):
        return len(self.get_alighting(floor)) > 0

    def clear_alighting(self, floor):
        self.alighting_people[floor - 1] = []
