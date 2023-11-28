from abc import ABC, abstractmethod
from enum import Enum

class Priority(Enum):
    PASSENGER = 1 
    MOVE = 2
    OTHER = 3

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
        return self.time > other.time or self.priority.value > other.priority.value

class PassengerEvent(Event):
    def __init__(self, time, floor, building):
        super().__init__(time, Priority.PASSENGER)
        self.floor = floor
        self.building = building
        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def __str__(self):
        return f"{super().__str__()}{self.describe()}"

    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def update(self):
        pass

class MoveEvent(Event):
    def __init__(self, time, floor, building):
        super().__init__(time, Priority.MOVE)
        self.floor = floor
        self.building = building
        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def __str__(self):
        return f"{super().__str__()}{self.describe()}"

    @abstractmethod
    def describe(self):
        pass

    @abstractmethod
    def update(self):
        pass




