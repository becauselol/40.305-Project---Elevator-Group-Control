import numpy as np

from classes.event import PassengerEvent
from classes.controller import Move
import classes.moveEvents as moveE
from classes.passenger import Passenger

class ArrivalEvent(PassengerEvent):
# need to add the external call
# triggers UpdateMoveEvent
# if elevator is idle/wait
    def __init__(self, time, floor, building, dest, rate):
        super().__init__(time, floor, building)
        self.source = floor
        self.dest = dest
        self.rate = rate

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
        self.controller.add_ext_call(self.floor, passenger.get_direction(), self.time)

        yield self.next_arrival_event()

        # elevator will only be updated if it is in IDLE or WAIT
        if self.elevator.direction in [Move.IDLE, Move.WAIT]:
            self.elevator.direction = Move.WAIT_UPDATE
            yield moveE.UpdateMoveEvent(self.time, self.floor, self.building)


class AlightEvent(PassengerEvent):
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

# will delete the internal calls
    def update(self):
        self.building.remove_passenger_from_elevator(self.floor)
        yield DepartureEvent(self.time, self.floor, self.building)


class DepartureEvent(PassengerEvent):
# triggers DoorCloseEvent
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def update(self):
        removed_passengers = self.building.remove_passenger_from_building(self.floor)

        # likewise, potentially can be removed if DoorOpenEvent
        # yields both DoorClose and AlightEvent
        yield moveE.DoorCloseEvent(self.time, self.floor, self.building)


class BoardEvent(PassengerEvent):
# will delete external calls
# add internal calls
# trigger NextFloorEvent
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def update(self):

        # board people
        internal_calls = self.building.add_passenger_to_elevator(self.floor, self.elevator.direction)

        # if there are any more ppl waiting, we add ext call again
        if (boarding_passengers := self.building.get_boarding(self.floor, self.elevator.direction)):
            # the first in the queue will be the min_spawn_time
            min_time = boarding_passengers[0].spawn_time
            self.controller.add_ext_call(self.floor, self.elevator.direction, min_time)

        # update the internal calls based on the boarded people
        for new_int_call in internal_calls:
            self.controller.add_int_call(new_int_call, self.elevator.direction)

        # potentially can be removed if DoorCloseEvent just yields this event as well
        yield moveE.NextFloorEvent(
                self.time + self.elevator.move_speed,
                self.floor + self.elevator.direction.value,
                self.building
            ) 


