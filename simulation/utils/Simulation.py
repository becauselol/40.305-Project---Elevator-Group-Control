from queue import PriorityQueue
from numpy.random import exponential

from classes.Building import Building
# from .DataStore import DataStore
from .Event import ArrivalEvent, PassengerEvent, MoveEvent, ReachFloorEvent, UpdateMoveEvent, StayIdleEvent


class Simulation:
    
    def __init__(self):
        pass    

    def simulate(self, max_time):
        self.arrival_queue = PriorityQueue()
        building = Building(1, 3, 3)
        elevator_events = [StayIdleEvent(0, building, 1, 0)]

        # initialize all the arrival events
        rates = [
                [0, 10, 10],
                [10, 0, 10],
                [10, 10, 0]
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

        while self.arrival_queue.queue[0][0] < max_time:
            # check if elevator_events or arrival_event first
            if  (not isinstance(elevator_events[0], StayIdleEvent)) and  elevator_events[0].time < self.arrival_queue.queue[0][0]:
                # Ensures that given the same execution time, we initiate the DoorOpen first to 
                event = elevator_events[0]

            else:
                event_time, event = self.arrival_queue.get()

            print(event)
            print(type(event))
            print("current elevator event:", type(elevator_events[0]))
            print("current elevator direction:", building.elevator.direction)
            if isinstance(elevator_events[0], ReachFloorEvent):
                print("current target floor:", elevator_events[0].alight_floor)
                print("start time:", elevator_events[0].prev_time)
                print("reach time:", elevator_events[0].time)
            print("current elevator floor:", building.elevator.current_floor)

            if isinstance(event, UpdateMoveEvent):
                new_events = event.update(elevator_events)
                print("UPDATED EVENT") 
                print(new_events)
            else:
                new_events = event.update()

            for e in new_events:
                if isinstance(e, PassengerEvent):
                    self.arrival_queue.put((e.time, e))
                elif isinstance(e, MoveEvent):
                    elevator_events[0] = e
                elif isinstance(e, UpdateMoveEvent):
                    self.arrival_queue.put((e.time, e))



        

