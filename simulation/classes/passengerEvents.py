import numpy as np

from .event import PassengerEvent, PassengerElevatorEvent
from .controller import Move
from . import moveEvents as moveE
from .passenger import Passenger

class ArrivalEvent(PassengerEvent):
# need to add the external call
# triggers UpdateMoveEvent
# if elevator is idle/wait
    def __init__(self, time, floor, building, dest, rate):
        super().__init__(time, floor, building)
        self.source = floor
        self.dest = dest
        self.rate = rate

    def describe(self):
        return f"Spawning from {self.source} -> {self.dest}"

    def next_arrival_event(self):
        return ArrivalEvent(
            self.time + np.random.exponential(self.rate), 
            self.floor, 
            self.building, 
            self.dest, 
            self.rate
        )

    def update(self):
        # add passenger to the floor
        passenger = Passenger(self.time, self.source, self.dest)
        self.building.add_passenger_to_floor(self.floor, passenger)
        # add the external call accordingly
        # check which elevator is this assigned to
        assigned_elevator = self.groupController.assign_call(self.floor, passenger.get_direction(), self.time)

        self.groupController.add_ext_call_to_lift(assigned_elevator, self.floor, passenger.get_direction(), self.time)

        yield self.next_arrival_event()

        # elevator will only be updated if it is in IDLE or WAIT
        # Check with the groupController, if it is a new call
        # If it is a new call that is not handled
        # Then we need to assign the call to a lift
        self.elevator = self.building.elevators[assigned_elevator]
        if self.elevator.direction in [Move.IDLE, Move.WAIT]:
            self.elevator.direction = Move.WAIT_UPDATE
            yield moveE.UpdateMoveEvent(self.time, self.floor, self.building, assigned_elevator)


class AlightEvent(PassengerElevatorEvent):
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Alighting {len(self.elevator.get_alighting(self.floor))} at {self.floor}"

# will delete the internal calls
    def update(self):
        self.building.remove_passenger_from_elevator(self.elevator_id, self.floor)
        yield DepartureEvent(self.time, self.floor, self.building)


class DepartureEvent(PassengerEvent):
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def describe(self):
        return f"Terminating {len(self.building.get_terminating(self.floor))} from {self.floor}"

    def update(self):
        self.removed_passengers = self.building.remove_passenger_from_building(self.floor, self.time)

        return
        yield

    def data_update(self):
        return self.removed_passengers


class BoardEvent(PassengerElevatorEvent):
# will delete external calls
# add internal calls
# trigger NextFloorEvent
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Boarding {len(self.building.get_boarding(self.floor, self.elevator.direction))} at {self.floor}"

    def update(self):

        # board people
        internal_calls = self.building.add_passenger_to_elevator(self.elevator_id, self.floor, self.elevator.direction, self.time)

        # CODE SHOULD BE IRRELEVANT SINCE ASSUMPTION IS ELEVATOR IS INFINITELY LARGE
        # if there are any more ppl waiting, we add ext call again
        if (boarding_passengers := self.building.get_boarding(self.floor, self.elevator.direction)):
            # the first in the queue will be the min_spawn_time
            min_time = boarding_passengers[0].spawn_time
            self.controller.add_ext_call(self.floor, self.elevator.direction, min_time)

        # update the internal calls based on the boarded people
        for new_int_call in internal_calls:
            self.controller.add_int_call(new_int_call, self.elevator.direction)

        # yields doorclose
        yield moveE.DoorCloseEvent(
                self.time,
                self.floor,
                self.building,
                self.elevator_id
                )
