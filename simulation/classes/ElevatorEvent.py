from queue import PriorityQueue
from .Elevator import Elevator

class ElevatorEvent:
    def __init__(self):
        self.event_queue = PriorityQueue()
        
