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

    @abstractmethod
    def update(self):
        pass

class PassengerEvent(Event):
    def __init__(self, time):
        super().__init__(time, Priority.PASSENGER)

    @abstractmethod
    def update(self):
        pass

class MoveEvent(Event):
    def __init__(self, time):
        super().__init__(time, Priority.MOVE)

    @abstractmethod
    def update(self):
        pass




