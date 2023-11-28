
from classes.controller import EqualController, Move
from classes.elevator import Elevator


class Building:
    def __init__(self, num_floors, min_floor=1):
        self.num_floors = num_floors
        self.min_floor = min_floor
        self.max_floor = num_floors
        self.elevator = Elevator(num_floors)
        self.controller = EqualController(num_floors)

        self.waiting_people = [
                {
                    Move.UP: [],
                    Move.DOWN: []
                }
                for _ in range(num_floors)
            ]
        self.alighted_people = [[] for _ in range(num_floors)]

    def get_terminating(self, floor):
        return self.alighted_people[floor - 1]

    def get_boarding(self, floor, move_direction):
        return self.waiting_people[floor - 1][move_direction]

    def check_boarding(self, floor, move_direction):
        return len(self.get_boarding(floor, move_direction)) > 0

    def add_passenger_to_floor(self, floor, passenger):
        self.waiting_people[floor - 1][passenger.get_direction()].append(passenger)


    def remove_passenger_from_elevator(self, floor):
        self.alighted_people[floor - 1] = self.elevator.get_alighting(floor)
        self.elevator.clear_alighting(floor)


    def remove_passenger_from_building(self, floor):
        removed_passengers = self.alighted_people[floor - 1]
        self.alighted_people[floor - 1] = []
        return removed_passengers

    
    def add_passenger_to_elevator(self, floor, move_direction):
        int_calls = set()
        remaining_passengers = []

        for passenger in self.waiting_people[floor - 1][move_direction]:
            if self.elevator.get_num_passengers() >= self.elevator.capacity:
                remaining_passengers.append(passenger)
                continue

            self.elevator.add_passenger(passenger)
            int_calls.add(passenger.dest)

        self.waiting_people[floor - 1][move_direction] = remaining_passengers

        return int_calls
