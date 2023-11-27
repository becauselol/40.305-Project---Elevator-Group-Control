from .Elevator import Elevator, ElevatorController, Move

class Building:
    
    def __init__(self, num_elevators, num_floors, elevator_capacity):
        self.num_elevators = num_elevators
        self.num_floors = num_floors
        self.waiting_people = [
                {
                    Move.UP: [],
                    Move.DOWN: []
                }
                for _ in range(num_floors)
            ]
        self.alighted_people = [[] for _ in range(num_floors)]

        self.elevator = Elevator(elevator_capacity, num_floors)
        self.controller = ElevatorController()

    def get_next_elevator_move(self):
        self.controller.next_floor(self.elevator)

    def add_passenger_to_floor(self, time, source_floor, passenger):
        direction = Move.UP if passenger.dest - passenger.source > 0 else Move.DOWN

        is_new_passenger = len(self.waiting_people[source_floor - 1][direction]) == 0
        self.waiting_people[source_floor - 1][direction].append(passenger)
        
        self.controller.add_floor(self.elevator, source_floor, True, time)

        return is_new_passenger


    def add_passenger_to_elevator(self, time, floor):
        # get current floor and direction
        
        move_direction = self.elevator.direction

        destinations = set()
        for passenger in self.waiting_people[floor][move_direction]:
            if self.elevator.get_num_passengers() >= self.elevator.capacity:
                break

            self.elevator.add_passenger(passenger)
            destinations.add(passenger.dest)
        

        for destination in destinations:
            self.controller.add_floor(self.elevator, destination, False, time)

    def remove_passenger_from_elevator(self, floor):
        self.alighted_people[floor - 1] = self.elevator.alighting_people[floor - 1]
        self.elevator.alighting_people[floor - 1] = []



            




