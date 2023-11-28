from classes.event import MoveEvent
import classes.passengerEvents as passE
from classes.controller import Move

"""
NOTE: time is the time that the event occurs
"""

class NextFloorEvent(MoveEvent):
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def describe(self):
        return f"Elevator reaching floor {self.floor}"

    def update(self):
        self.elevator.floor = self.floor
        next_floor = self.controller.where_next_moving(self.elevator.floor, self.elevator.direction)

        if next_floor == self.floor:
            yield DoorOpenEvent(self.time, self.floor, self.building)
            return
            # yield a door open event

        yield NextFloorEvent(
                self.time + self.elevator.move_speed,
                self.floor + self.elevator.direction.value,
                self.building
            ) 

class DoorOpenEvent(MoveEvent):
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def describe(self):
        return f"Elevator opening door at {self.floor}"

    def update(self):
        # consume the internal and external call
        self.controller.consume_int_call(self.floor, self.elevator.direction)
        self.controller.consume_ext_call(self.floor, self.elevator.direction)
        # Check if anyone alighting
        if self.elevator.check_alighting(self.floor):
            # trigger an alight event
            yield passE.AlightEvent(self.time, self.floor, self.building)
            return

        # regardless, we then need to trigger a 
        # DoorCloseEvent and see what the next steps are
        yield DoorCloseEvent(
                    self.time + self.elevator.open_door_time,
                    self.floor,
                    self.building
                )


class DoorCloseEvent(MoveEvent):
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def describe(self):
        return f"Elevator closing door at {self.floor}"

    def update(self):
        # update the elevators movement
        if not (boarding_check:= self.building.check_boarding(self.floor, self.elevator.direction)):
            self.elevator.direction = self.controller.where_next_stationary(self.elevator.floor, self.elevator.direction)

        match self.elevator.direction:
            case Move.UP | Move.DOWN:
                if boarding_check:
                    # trigger a board event:
                    yield passE.BoardEvent(self.time, self.floor, self.building)
                    return

                # then make sure we trigger a next floor event 
                # that happens AFTER the board event
                yield NextFloorEvent(
                        self.time + self.elevator.move_speed,
                        self.floor + self.elevator.direction.value,
                        self.building
                    )
                return

            case Move.WAIT:
                # If the elevator is already at idle
                if self.controller.at_idle(self.elevator):
                    # We set the state to idle
                    self.elevator.direction = Move.IDLE
                    # Let the elevator stay at IDLE
                    return

                yield MoveIdleEvent(
                        self.time + self.elevator.wait_to_idle,
                        self.floor,
                        self.building
                    )

                
class MoveIdleEvent(MoveEvent):
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def describe(self):
        return f"Moving to IDLE floor {self.controller.get_idle_floor(self.elevator)}"

    def update(self):
        # now that it is triggered, it should trigger a movement that allows the waiting elevator to move to the idle state
        
        # also set the elevator to a special state that cannot be disturbed
        self.elevator.direction = Move.MOVE_TO_IDLE

        # calculate the time it takes to reach the idle floor
        time_to_move_to_idle = self.controller.time_to_idle_floor(self.elevator)
        idle_floor = self.controller.get_idle_floor(self.elevator)

        yield ReachIdleEvent(self.time + time_to_move_to_idle , idle_floor, self.building)


class ReachIdleEvent(MoveEvent):
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def describe(self):
        return f"Reached the IDLE state at {self.floor}"

    def update(self):
        self.elevator.direction = Move.IDLE
        self.elevator.floor = self.floor

        # check if there are any calls
        # If yes, we should do a NextFloor
        if not self.controller.request_is_empty():
            yield UpdateMoveEvent(self.time, self.floor, self.building)


class UpdateMoveEvent(MoveEvent):
    """
    Only called when the lift is in IDLE/WAIT
    will allow respond to the closest
    """
    def __init__(self, time, floor, building):
        super().__init__(time, floor, building)

    def describe(self):
        return f"Elevator was in IDLE/WAIT, updating move"

    def update(self):
        if self.elevator.direction == Move.MOVE_TO_IDLE:
            raise Error("Moving to Idle, this event can't occur")
        # First remove any WaitIdleEvents in the queue
        if self.elevator.direction == Move.WAIT:
            # we need to eliminate the MoveIdleEvent
            pass

        # We also need to change the state of the elevator
        # Check what direction to move in
        self.elevator.direction = self.controller.check_direction(self.elevator.floor)

        # now check where to move
        # does so by triggering a NextFloorEvent
        # without any delay
        yield NextFloorEvent(self.time, self.floor, self.building)







