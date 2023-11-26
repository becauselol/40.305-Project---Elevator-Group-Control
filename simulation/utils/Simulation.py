from queue import PriorityQueue
from numpy.random import exponential

from ..classes.Building import Building
# from .DataStore import DataStore
from .Event import ArrivalEvent, PassengerEvent, MoveEvent, UpdateMoveEvent


class Simulation:
    
    def __init__(self):
        pass    

    def simulate(self, max_time):
        self.arrival_queue = PriorityQueue()
        building = Building(1, 3, 3)
        elevator_events = [None]

        # initialize all the arrival events
        rates = [
                [0, 1, 1],
                [1, 0, 1],
                [1, 1, 0]
            ]

        for i in range(3):
            for j in range(3):
                if i == j:
                    continue
                arrival_time = exponential(rates[i][j])
                event = ArrivalEvent(
                        arrival_time,
                        building,
                        i + 1,
                        j + 1,
                        rates[i][j]
                    )

                self.arrival_queue.put((arrival_time, event))

        while self.arrival_queue[0][0] < max_time:
            # check if elevator_events or arrival_event first
            if elevator_events[0].time < self.arrival_queue[0][0]:
                event = elevator_events[0]

            else:
                event = self.arrival_queue.get()

            print(event)

            if isinstance(event, UpdateMoveEvent):
                new_events = event.update(elevator_events)
            else:
                new_events = event.update()

            for e in new_events:
                if isinstance(e, PassengerEvent):
                    self.arrival_queue.put((e.time, e))
                elif isinstance(e, MoveEvent):
                    elevator_events[0] = e
                elif isinstance(e, UpdateMoveEvent):
                    self.arrival_queue.put((e.time, e))


        

