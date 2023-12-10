from .event import MoveEvent, ElevatorEvent
from . import passengerEvents as passE
from .controller import Move
from .elevator import State

"""
NOTE: time is the time that the event occurs

# Sequence of events when it reaches the correct floor
# CONDITION: elevator is moving in direction up
0. Elevator reaches the floor
    What this means is that we eliminate any internal calls and any external calls

    DOOR OPEN --> triggers ALIGHT if alighting, triggers BOARD if boarding, triggers DOOR CLOSE

1. Check if there is anyone alighting

    ALIGHT --> triggers DEPARTURE

2. Alight people
3. wait for a bit
4. check if there is anyone who wants to board in the direction up

    BOARD --> triggers DOOR CLOSE

5. if yes, board them
    update the internal calls

    DOOR CLOSE --> trigger DOOR OPEN if change direction, trigger MOVE TO IDLE if wait, trigger NEXT FLOOR if no change

6. check if we need to change direction
    7. check if there are any people in the lift who still want to go up
    8. check if there are any calls above it that need to respond to
9. if no need to change direction
10. carry on    NEXT FLOOR

11. check if there are any calls below this floor as well (this includes anyone who wants to board on this floor)

    DOOR OPEN --> trigger BOARD if boarding else DOOR CLOSE

12. if yes, change direction
    This then means we eliminate the external call that is to go down
13. check if there is anyone who wants to board in the direction down

    BOARD --> triggers DOOR CLOSE

14. if yes, board them
    update the internal calls

    DOOR CLOSE --> trigger DOOR OPEN if change direction, trigger MOVE TO IDLE if wait, trigger NEXT FLOOR if no change

14. carry on    NEXT FLOOR

15. If no then just change state to WAIT 

    MOVE TO IDLE

16. And also add event to trigger the movement to Idle

"""

# These events are specific to a certain elevator
# Each event now needs to take in a new parameter
# The elevator ID
class NextFloorEvent(ElevatorEvent):
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Elevator {self.elevator_id} floor {self.elevator.floor} -> {self.floor}"

    def update(self):
        self.elevator.floor = self.floor
        next_floor = self.controller.where_next_moving(self.elevator.floor, self.elevator.direction)

        if next_floor == self.floor:
            yield DoorOpenEvent(self.time, self.floor, self.building, self.elevator_id)
            return
            # yield a door open event

        yield NextFloorEvent(
                self.time + self.elevator.move_speed,
                self.floor + self.elevator.direction.value,
                self.building, self.elevator_id
            ) 

class DoorOpenEvent(ElevatorEvent):
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Elevator {self.elevator_id} opening door at {self.floor}"

    def update(self):
        # consume the internal and external call
        self.controller.consume_int_call(self.floor, self.elevator.direction)

        self.elevator.direction = self.controller.where_next_stationary(self.elevator.floor, self.elevator.direction)

        self.controller.consume_ext_call(self.floor, self.elevator.direction)

        # Check if anyone alighting
        if self.elevator.check_alighting(self.floor):
            # trigger an alight event
            yield passE.AlightEvent(self.time, self.floor, self.building, self.elevator_id)

        # always try to board even if there is no one this is so we will check
        # as long as there is movement
        if self.elevator.direction != Move.NONE:
            yield passE.BoardEvent(self.time + self.elevator.open_door_time, self.floor, self.building, self.elevator_id)

        # if there is no movement, go straight to door close
        else:
            yield DoorCloseEvent(self.time + self.elevator.open_door_time, self.floor, self.building, self.elevator_id)



class DoorCloseEvent(ElevatorEvent):
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Elevator {self.elevator_id} closing door at {self.floor}"

    def update(self):
        # update the elevators movement

        match self.elevator.direction:
            case Move.NONE:
                if self.elevator.floor == self.controller.get_idle_floor(self.elevator):
                    yield ReachIdleEvent(self.time, self.floor, self.building, self.elevator_id)
                    return
                else:
                    self.elevator.state = State.MOVING_TO_IDLE
                    yield MoveIdleEvent(
                            self.time + self.elevator.wait_to_idle,
                            self.floor,
                            self.building, self.elevator_id
                            )
                    return        
            # if it is moving, we just go
            case _:
                yield NextFloorEvent(
                        self.time + self.elevator.move_speed,
                        self.floor + self.elevator.direction.value,
                        self.building, self.elevator_id
                        )
                return

                
class MoveIdleEvent(ElevatorEvent):
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Elevator {self.elevator_id} moving to IDLE floor {self.controller.get_idle_floor(self.elevator)}"

    def update(self):
        # now that it is triggered, it should trigger a movement that allows the waiting elevator to move to the idle state
        
        # also set the elevator to a special state that cannot be disturbed
        self.elevator.state = State.MOVING_TO_IDLE

        # calculate the time it takes to reach the idle floor
        time_to_move_to_idle = self.controller.time_to_idle_floor(self.elevator)
        idle_floor = self.controller.get_idle_floor(self.elevator)

        yield ReachIdleEvent(self.time + time_to_move_to_idle , idle_floor, self.building, self.elevator_id)


class ReachIdleEvent(ElevatorEvent):
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Elevator {self.elevator_id} reached the IDLE state at {self.floor}"

    def update(self):
        self.elevator.direction = Move.IDLE
        self.elevator.floor = self.floor

        # check if there are any calls
        # If yes, we should do a NextFloor
        if not self.controller.request_is_empty():
            yield UpdateMoveEvent(self.time, self.floor, self.building, self.elevator_id)


class UpdateMoveEvent(ElevatorEvent):
    """
    Only called when the lift is in IDLE/WAIT
    will allow respond to the closest
    """
    def __init__(self, time, floor, building, elevator_id):
        super().__init__(time, floor, building, elevator_id)

    def describe(self):
        return f"Elevator {self.elevator_id} was in IDLE/WAIT, updating move"

    def update(self):
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
        yield NextFloorEvent(self.time, self.elevator.floor, self.building, self.elevator_id)
