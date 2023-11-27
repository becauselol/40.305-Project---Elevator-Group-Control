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
        self.controller = ElevatorController(num_floors)


    def add_passenger_to_floor(self, time, source_floor, passenger):
        direction = Move.UP if passenger.dest - passenger.source > 0 else Move.DOWN

        is_new_passenger = len(self.waiting_people[source_floor - 1][direction]) == 0
        self.waiting_people[source_floor - 1][direction].append(passenger)
        
        self.controller.add_ext_call(time, self.elevator, source_floor, direction)

        return is_new_passenger


    def add_passenger_to_elevator(self, time, floor):
        # get current floor and direction
        
        move_direction = self.elevator.direction

        destinations = set()
        remaining_passengers = []
        for passenger in self.waiting_people[floor - 1][move_direction]:
            if self.elevator.get_num_passengers() >= self.elevator.capacity:
                remaining_passengers.append(passenger)
                continue

            self.elevator.add_passenger(passenger)
            destinations.add(passenger.dest)

        if len(remaining_passengers) == 0:
            self.controller.consume_ext_call(floor, move_direction)
        else:
            # find the earliest arrival
            # The one at the front of the queue should be the earliest spawn time
            next_earliest_arrival = remaining_passengers[0].spawn_time
            self.controller.update_ext_call_priority(floor, move_direction, next_earliest_arrival)

        self.waiting_people[floor - 1][move_direction] = remaining_passengers
        

        for destination in destinations:
            self.controller.add_int_call(time, self.elevator, destination)

    def remove_passenger_from_elevator(self, floor):

        self.alighted_people[floor - 1] = self.elevator.alighting_people[floor - 1]

        # Call should be consumed
        # if len(self.elevator.alighting_people[floor - 1]) > 0:
        #     self.controller.consume_int_call(floor, self.elevator.direction)

        self.elevator.alighting_people[floor - 1] = []



            




