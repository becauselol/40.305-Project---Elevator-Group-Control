from abc import ABC

class Event(ABC):
    def __init__(self, time):
        self.time = time

    @abstractmethod
    def update(self):
        pass

class ArrivalEvent(Event):
    def __init__(self, time, building, passenger):
        self.time = time
        self.passenger = passenger
        self.building = building

    def update()
