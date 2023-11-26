from abc import ABC, abstractmethod
from numpy.random import exponential
from ..classes.Passenger import Passenger

class Event(ABC):
    def __init__(self, time):
        self.time = time

    def __str__(self):
        return f"Time {self.time:6.2f}: "

    @abstractmethod
    def update(self):
        pass

class PassengerEvent(Event):
    def __init__(self, time):
        self.time = time

    @abstractmethod
    def update(self):
        pass

class MoveEvent(Event):
    def __init__(self, time):
        self.time = time    

    @abstractmethod
    def update(self):
        pass


class ArrivalEvent(PassengerEvent):
    """
    Event that deals with the addition of passengers to the building
    """
    def __init__(self, time, building, source, dest, rate):
        self.time = time
        self.building = building
        self.source = source
        self.dest = dest
        self.rate = rate

    def __str__(self):
        return f"{super().__str__()}Spawning Passenger going from {self.source} to {}"

    def update(self):
        new_passenger = Passenger(self.time, self.source, self.dest)
        is_new_passenger = self.building.add_passenger_to_floor(self.source, new_passenger)
        
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
        self.time = time
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}Removing People from {self.floor}"

    def update(self):
        self.building.alighted_people[self.floor - 1] = []


class AlightEvent(PassengerEvent):
    
    def __init__(self, time, building, floor):
        self.time = time
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}Alighting People from {self.floor}"

    def update(self):
        self.building.remove_passenger_from_elevator(self.floor)

        # This then triggers the board event, if anyone is boarding
        new_events = [
                DepartureEvent(
                    self.time,
                    self.building,
                    self.floor
                )
            ]

        if self.building.check_passenger_boarding(self.floor):
            new_events.append(
                    BoardEvent(
                        self.time + self.building.elevator.wait_time,
                        self.building,
                        self.floor
                    )
                )
        else:
            new_events.append(
                    UpdateMoveEvent(
                        self.time + self.building.elevator.wait_time,
                        self.building
                    )
                )
        # If no one is boarding, it trggers a UpdateMoveEvent instead
        # And a departure event
        return new_events
        

class BoardEvent(PassengerEvent):
    
    def __init__(self, time, building, floor):
        self.time = time
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}Boarding People from {self.floor}"

    def update(self):
        self.building.add_passenger_to_elevator(self.floor)

        return [
            UpdateMoveEvent(
                self.time,
                self.building
            )
        ]



class UpdateMoveEvent(Event):
    """
    Updates the MoveEvents
    """
    def __init__(self, time, building):
        self.time = time
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
            ReachFloorEvent (Regardless of if last Event was ArrivalEvent or BoardEvent)
            StayIdleEvent (Elevator has reached Idle position, now ready to respond to new calls)
            WaitEvent (Elevator is waiting for call but not ready to move to Idle position)
            MoveIdleEvent (Elevator is moving to an Idle position and cannot respond)

        Who calls this Event?:
            ArrivalEvent (We will check if ReachFloorEvent needs to be modified to Reach an earlier floor along it's path)
            AlightEvent/BoardEvent (Check what is the next ReachFloorEvent we need to create)
            StayIdleEvent (Check if there are any calls to respond to once it reaches Idle) (This is a necessary condition, since ReachFloorEvent cannot be created when Elevator is in MoveIdleEvent. ArrivalEvent will not trigger any ReachFloorEvent when Elevator is in MoveIdleEvent)
        """
        # Check what the next correct move is for the elevator

        # If no current calls, wait until the time to move to idle
        if self.building.controller.request_is_empty():
            return [
                WaitEvent(
                    self.time + self.building.controller.wait_time,
                    self.building,
                    self.time
                )
            ]
        next_move = self.building.controller.get_next_elevator_move()
        
        

        return next_move

class ReachFloorEvent(MoveEvent):
    """
    Collated Event that handles what happens when a 
    Elevator reaches a floor
    """
    def __init__(self, time, building, floor, prev_time):
        self.time = time,
        self.building = building
        self.floor = floor
        self.prev_time = prev_time

    def __str__(self):
        return f"{super().__str__()}Reached Floor {self.floor}"

    def update(self):
        """
        It should trigger a AlightEvent
        """
        
        return [
            AlightEvent(
                self.time,
                self.building,
                self.floor
            )
        ]

class WaitEvent(Event):
    """
    In this state, the Elevator can be disturbed and moved to another location
    """
    def __init__(self, time, building, start_idle_time):
        self.time = time,
        self.building = building
        self.start_idle_time = start_idle_time

    def update(self):
        # Once it starts moving to the Idle state, it cannot be stopped, until it reaches its idle state
        return [
            MoveIdleEvent(
                self.time,
                self.building,
                self.building.controller.move_idle_direction(self.building.elevator)
            )
        ]

class StayIdleEvent(Event):
    """
    In this state, the Elevator can be disturbed and moved to another location
    """
    def __init__(self, time, building, start_idle_time):
        self.time = time,
        self.building = building
        self.start_idle_time = start_idle_time
    
    def __str__(self):
        return f"{super().__str__()}Stay Idle since {self.start_idle_time}"

    def update(self):
        """
        It should check if there are new events to attend to. Otherwise, stay idle
        """
        return [
            UpdateMoveEvent(
                self.time,
                self.building
            )
        ]

class MoveIdleEvent(Event):
    """
    Event that triggers a move to idle position
    Elevator cannot be interrupted during this sequence
    """
    def __init__(self, time, building, floor):
        self.time = time,
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}At Floor {self.floor}, Moving to Idle"

    def update(self):
        elevator = self.building.elevator
        controller = self.building.controller
        if self.floor != controller.get_idle_floor(elevator):
            return [
                MoveIdleEvent(
                    self.time + elevator.move_speed,
                    self.building,
                    self.floor + controller.move_idle_direction(elevator)
                )    
            ]

        
        # otherwise reach already
        return [
            StayIdleEvent(
                self.time,
                self.building,
                self.time
            )
        ]
