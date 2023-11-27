from abc import ABC, abstractmethod
from enum import Enum
from numpy import nextafter
from numpy.random import exponential
from classes.Passenger import Passenger
from classes.Elevator import Move

class Priority(Enum):
    ARRIVAL = 1 
    BOARD = 2
    UPDATE = 3
    OTHER = 4

# Priority ensures that we update then we board



class Event(ABC):
    def __init__(self, time, priority):
        self.time = time
        self.priority = priority

    def __str__(self):
        return f"Time {self.time:6.6f}: "

    @abstractmethod
    def update(self):
        pass

    def __gt__(self, other):
        if isinstance(other, Event):
            return self.time > other.time or self.priority.value < other.priority.value


class PassengerEvent(Event):
    def __init__(self, time, priority):
        super().__init__(time, priority)

    @abstractmethod
    def update(self):
        pass

class MoveEvent(Event):
    def __init__(self, time, priority):
        super().__init__(time, priority)

    @abstractmethod
    def update(self):
        pass


class ArrivalEvent(PassengerEvent):
    """
    Event that deals with the addition of passengers to the building
    """
    def __init__(self, time, building, source, dest, rate):
        super().__init__(time, Priority.ARRIVAL)
        self.building = building
        self.source = source
        self.dest = dest
        self.rate = rate

    def __str__(self):
        return f"{super().__str__()}Spawning Passenger going from {self.source} to {self.dest}"

    def update(self):
        new_passenger = Passenger(self.time, self.source, self.dest)
        is_new_passenger = self.building.add_passenger_to_floor(self.time, self.source, new_passenger)
        
        # generate the new event to add the next passenger
        
        new_time = self.time + exponential(self.rate)

        new_events =  [
            ArrivalEvent(
                    self.time + new_time,
                    self.building,
                    self.source,
                    self.dest,
                    self.rate
                )
            ]
        
        # Check if the current MoveEvents are correct
        # Otherwise update the MoveEvent
        if is_new_passenger:
            new_events.append(
                    UpdateMoveEvent(
                            self.time,
                            self.building
                        )
                )
        
        return new_events

class DepartureEvent(PassengerEvent):
    
    def __init__(self, time, building, floor):
        super().__init__(time, Priority.OTHER)
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}Removing {len(self.building.alighted_people[self.floor - 1])} People from Floor {self.floor}"

    def update(self):
        self.building.alighted_people[self.floor - 1] = []
        return []

class AlightEvent(PassengerEvent):
    
    def __init__(self, time, building, floor):
        super().__init__(time, Priority.OTHER)
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}Alighting {len(self.building.elevator.alighting_people[self.floor - 1])} People from {self.floor}"

    def update(self):
        self.building.remove_passenger_from_elevator(self.floor)

        # This then triggers the DepartureEvent since passengers
        # need to leave the system
        return [
                DepartureEvent(
                    self.time,
                    self.building,
                    self.floor
                )
            ]


class BoardEvent(PassengerEvent):
    
    def __init__(self, time, building, floor):
        super().__init__(time, Priority.BOARD)
        self.building = building
        self.floor = floor

    def __str__(self):
        elevator = self.building.elevator
        return f"{super().__str__()}Boarding {len(self.building.waiting_people[self.floor - 1][elevator.direction])} People from {self.floor}"

    def update(self):
        self.building.add_passenger_to_elevator(self.time, self.floor)
        return []


class UpdateMoveEvent(Event):
    """
    Updates the MoveEvents
    """
    def __init__(self, time, building):
        super().__init__(time, Priority.UPDATE)
        self.building = building

    def __str__(self):
        return f"{super().__str__()}Updating the MoveEvent for Elevator"

    def update(self, elevator_events):
        """
        Check what the correct next move is for the Elevator and Return it
        Will return either a ReachFloorEvent or a MoveIdleEvent

        ReachFloorEvent implies they currently have a call and are responding
        MoveIdleEvent implies no calls and the intention is to move to the Idle State

        When UpdateMoveEvent is called, there are a few states for the ElevatorEvents
        Elevator Event:
            ReachFloorEvent (Last event has to be a ArrivalEvent)
            DoorOpenEvent (Waiting to see what the next call is)
            StayIdleEvent (Elevator has reached Idle position, now ready to respond to new calls)
            WaitEvent (Elevator is waiting for call but not ready to move to Idle position)
            MoveIdleEvent (Elevator is moving to an Idle position and cannot respond)

        Who calls this Event?:
            ArrivalEvent (We will check if ReachFloorEvent needs to be modified to Reach an earlier floor along it's path)
            DoorOpenEvent (Check what is the next ReachFloorEvent we need to create)
            StayIdleEvent (Check if there are any calls to respond to once it reaches Idle) (This is a necessary condition, since ReachFloorEvent cannot be created when Elevator is in MoveIdleEvent. ArrivalEvent will not trigger any ReachFloorEvent when Elevator is in MoveIdleEvent)
        """
        # Check what the next correct move is for the elevator

        # If no current calls, wait until the time to move to idle
        # Check if lift is in motion
        # being on a ReachFloorEvent implies being in motion

        elevator = self.building.elevator
        event = elevator_events[0]
        moving = isinstance(event, ReachFloorEvent)
        current_move_floor = event.alight_floor if moving else -1
        next_floor = self.building.controller.check_next_move(self.time, elevator, moving, current_move_floor)
        print(elevator.direction)
        print(next_floor)

        if isinstance(event, ReachFloorEvent):
            # We want to check if the new call would affect
            # If it doesn't affect the motion, we just return
            reachFloorEventParams = event.to_dict()
            reachFloorEventParams["alight_floor"] = next_floor
            
            return [
                ReachFloorEvent(**reachFloorEventParams)
            ]

        elif isinstance(elevator_events[0], DoorOpenEvent):
            # Door was open and now we waiting to update to move to the next place
            # Now I need to consume the current call

            nextEventParams = {}
            nextEventParams["building"] = self.building
            latest_time = elevator_events[0].time

            wait = (next_floor == -1)
            if wait: 
                nextEventParams["time"] = latest_time + elevator.wait_idle_time
                nextEventParams["floor"] = elevator.current_floor
                nextEventParams["start_idle_time"] = self.time

                return [
                    WaitEvent(**nextEventParams)
                ]
            else:
                nextEventParams["time"] = latest_time + elevator.move_speed
                nextEventParams["floor"] = elevator.current_floor + elevator.direction.value
                nextEventParams["alight_floor"] = next_floor
                nextEventParams["prev_time"] = self.time

                return [
                    ReachFloorEvent(**nextEventParams)
                ]

        elif isinstance(event, StayIdleEvent) or isinstance(event, WaitEvent):
            # If there is no event, wait continue
            if next_floor == -1: return []
            nextEventParams = {}
            # Otherwise respond
            nextEventParams["building"] = self.building
            nextEventParams["time"] = self.time + elevator.move_speed
            nextEventParams["floor"] = elevator.current_floor + elevator.direction.value
            nextEventParams["alight_floor"] = next_floor
            nextEventParams["prev_time"] = self.time
            return [
                ReachFloorEvent(**nextEventParams)
            ]

        elif isinstance(elevator_events[0], MoveIdleEvent):
            # Cannot be disturbed
            return []
        else:
            return []
        

class ReachFloorEvent(MoveEvent):
    """
    Collated Event that handles what happens when a 
    Elevator reaches a floor
    """
    def __init__(self, time, building, floor, alight_floor, prev_time):
        """
        floor: Next floor it is about to reach
        alight_floor: Destination floor it will DoorOpen at
        time: Time that floor will be reached
        prev_time: Time the elevator started moving
        """
        super().__init__(time, Priority.OTHER)
        self.building = building
        self.floor = floor
        self.alight_floor = alight_floor
        self.prev_time = prev_time

    def __str__(self):
        return f"{super().__str__()}Reached Floor {self.floor}"

    def to_dict(self):
        return {
            "time": self.time,
            "building": self.building,
            "floor": self.floor,
            "alight_floor": self.alight_floor,
            "prev_time": self.prev_time
        }

    def update(self):
        """
        It should trigger the following events:
            - AlightEvent
            - BoardEvent
            - DoorOpenEvent
        """
        print("target floor:", self.alight_floor)
        elevator = self.building.elevator
        elevator.current_floor = self.floor
        if self.floor != self.alight_floor:
            return [
                ReachFloorEvent(
                    self.time + elevator.move_speed,
                    self.building,
                    self.floor + elevator.direction.value,
                    self.alight_floor,
                    self.prev_time
                )
            ]


        # Call this to check what the next direction of the lift is
        # The idea is if no more higher/lower calls to respond to, 
        # it should then start looking down/up

        # Consume the call first
        self.building.controller.consume_int_call(self.floor, self.building.elevator.direction)

        return [
            AlightEvent(
                self.time,
                self.building,
                self.floor
            ),
            DoorOpenEvent(
                self.time + elevator.wait_time,
                self.building,
                self.floor,
                self.time
            )
        ]

class DoorOpenEvent(MoveEvent):
    """
    Elevator reaches a floor and the door is now open
    """
    def __init__(self, time, building, floor, prev_time):
        super().__init__(time, Priority.OTHER)
        self.building = building
        self.floor = floor
        self.prev_time = prev_time

    def __str__(self):
        return f"{super().__str__()}About to leave Floor {self.floor}"

    def update(self):
        """
        It should trigger a UpdateMoveEvent
        when it is updating, basically means this event is over
        Doors are now closing
        """
        return [
            BoardEvent(
                self.time,
                self.building,
                self.floor
            ),
            UpdateMoveEvent(
                self.time,
                self.building
            )
        ]


class WaitEvent(MoveEvent):
    """
    In this state, the Elevator can be disturbed and moved to another location
    """
    def __init__(self, time, building, floor, start_idle_time):
        super().__init__(time, Priority.OTHER)
        self.building = building
        self.floor = floor
        self.start_idle_time = start_idle_time

    def __str__(self):
        return f"{super().__str__()}Waiting at floor {self.floor}"

    def update(self):
        # Once it starts moving to the Idle state, it cannot be stopped, until it reaches its idle state
        self.building.elevator.current_floor = self.floor
        return [
            MoveIdleEvent(
                self.time,
                self.building,
                self.building.controller.get_idle_floor(self.building.elevator)
            )
        ]

class StayIdleEvent(MoveEvent):
    """
    In this state, the Elevator can be disturbed and moved to another location
    """
    def __init__(self, time, building, floor, start_idle_time):
        super().__init__(time, Priority.OTHER)
        self.building = building
        self.floor = floor
        self.start_idle_time = start_idle_time
    
    def __str__(self):
        return f"{super().__str__()}Stay Idle since {self.start_idle_time}"

    def update(self):
        """
        It should check if there are new events to attend to. Otherwise, stay idle
        """
        self.building.elevator.current_floor = self.floor
        return [
            UpdateMoveEvent(
                self.time,
                self.building
            )
        ]

class MoveIdleEvent(MoveEvent):
    """
    Event that triggers a move to idle position
    Elevator cannot be interrupted during this sequence
    """
    def __init__(self, time, building, floor):
        super().__init__(time, Priority.OTHER)
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}At Floor {self.floor}, Moving to Idle"

    def update(self):
        elevator = self.building.elevator
        controller = self.building.controller
        elevator.current_floor = self.floor
        if self.floor != controller.get_idle_floor(elevator):
            return [
                MoveIdleEvent(
                    self.time + elevator.move_speed,
                    self.building,
                    self.floor + controller.move_idle_direction(elevator)
                )    
            ]

        
        # otherwise reach already
        self.building.elevator.direction == Move.IDLE
        return [
            StayIdleEvent(
                self.time,
                self.building,
                self.floor,
                self.time
            )
        ]
