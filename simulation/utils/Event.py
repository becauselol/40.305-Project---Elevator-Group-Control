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


class UpdateMoveEvent(Event):
    """
    Updates the MoveEvents
    """
    def __init__(self, time, building):
        self.time = time
        self.building = building

    def __str__(self):
        return f"{super().str__()}Updating the MoveEvent for Elevator"

    def update(self):
        # Check what the next correct move is for the elevator
        next_move = self.building.controller.get_next_elevator_move()
        

        return next_move

class ReachFloorEvent(MoveEvent):
    """
    Collated Event that handles what happens when a 
    Elevator reaches a floor
    """
    def __init__(self, time, building, floor):
        self.time = time,
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}Reached Floor {self.floor}"

    def update(self):
        """
        It should trigger the next correct MoveEvent
        """
        # If no one to alight and no one to board
        elevator = self.building.elevator
        waiting_people = self.building.waiting_people[elevator.direction]
        
        if len(elevator.alighting_people[self.floor - 1]) == 0 or len(waiting_people) == 0:

        # just go to next floor
            return [
                ReachFloorEvent(
                    self.time + elevator.move_speed,
                    self.building,
                    self.floor + elevator.direction
                    )
            ]
        

        # Otherwise, need to trigger open door and LeaveFloorEvent
        # Alight passengers
        self.building.remove_passenger_from_elevator(self.floor)

        return [
            LeaveFloorEvent(
                self.time + elevator.wait_time,
                self.building,
                self.floor
                ),
            DepartureEvent(
                self.time,
                self.building,
                self.floor
                )
        ]
        
class LeaveFloorEvent(MoveEvent):
    """
    Event that occurs after 
    """
    def __init__(self, time, building, floor):
        self.time = time
        self.building = building
        self.floor = floor

    def __str__(self):
        return f"{super().__str__()}Leave Floor {self.floor}"

    def update(self, next_passenger_time):
        # We should Board Passengers
        elevator = self.building.elevator
        controller = self.building.controller
        if next_passenger_time - self.time > controller.move_idle_duration(elevator):
            return [
                MoveIdleEvent(
                    self.time + elevator.move_speed,
                    self.building,
                    self.floor + controller.move_idle_direction(elevator)
                )
            ]
        
        # Otherwise board passengers
        self.building.add_passenger_to_elevator(self.floor)

        return [
            ReachFloorEvent(
                self.time + elevator.move_speed,
                self.building,
                self.floor + elevator.direction
                )
        ]


class StayIdleEvent(Event):
    def __init__(self, time, building):
        self.time = time,
        self.building = building
        self.start_idle_time = time
    
    def __str__(self):
        return f"{super().__str__()}Stay Idle since {self.start_idle_time}"

    def update(self):
        return None

class MoveIdleEvent(Event):
    """
    Event that triggers a move to idle position
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
                self.building
            )
        ]
