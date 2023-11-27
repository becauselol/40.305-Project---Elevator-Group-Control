from queue import PriorityQueue
from numpy.random import exponential

from classes.Building import Building
from classes.Elevator import Move
# from .DataStore import DataStore
from .Event import ArrivalEvent, DoorOpenEvent, MoveIdleEvent, PassengerEvent, MoveEvent, ReachFloorEvent, UpdateMoveEvent, StayIdleEvent, WaitEvent


class Simulation:
    
    def __init__(self):
        pass    

    def print_building_state(self, building):
        print("-" * 20)
        print("""BUILDING STATE""")
        print("-" * 20)
        for i in range(len(building.waiting_people) - 1, -1, -1):
            print(f"floor: {i + 1} " + "-" * 10)
            print("waiting up  :", len(building.waiting_people[i][Move.UP]))
            print("waiting down:", len(building.waiting_people[i][Move.DOWN]))
            print("-" * 20)


    def print_elevator_state(self, elevator, elevator_event):
        print("-" * 20)
        print("""ELEVATOR STATE""")
        print("current floor:", elevator.current_floor)
        print("current state:", elevator.direction)
        print("-" * 20)
        for i in range(len(elevator.alighting_people) - 1, -1, -1):
            print(f"floor: {i + 1} " + "-" * 10)
            print("Number alighting:", len(elevator.alighting_people[i]))
            print("-" * 20)

        if isinstance(elevator_event, DoorOpenEvent):
            print("State: Waiting to get new event")
        elif isinstance(elevator_event, ReachFloorEvent):
            print("State: Moving to next floor", elevator_event.alight_floor, "but currently otw to", elevator_event.floor)
        elif isinstance(elevator_event, StayIdleEvent):
            print("State: Idle since", elevator_event.start_idle_time)
        elif isinstance(elevator_event, MoveIdleEvent):
            print("State: Moving to Idle State")
        elif isinstance(elevator_event, WaitEvent):
            print("State: Waiting for next event")

        print("-"*20)


    def print_event(self, event):
        print("-" * 20)
        print("""EVENT STATE""")
        print("-" * 20)
        print(event)
        print("-" * 20)

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

            self.print_event(event)
            print("BEFORE")
            self.print_building_state(building)
            self.print_elevator_state(building.elevator, elevator_events[0])

            if isinstance(event, UpdateMoveEvent):
                new_events = event.update(elevator_events)
                print("UPDATED EVENT") 
                if new_events:
                    print(new_events[0].time)
            else:
                new_events = event.update()

            for e in new_events:
                if isinstance(e, PassengerEvent):
                    self.arrival_queue.put((e.time, e))
                elif isinstance(e, MoveEvent):
                    elevator_events[0] = e
                elif isinstance(e, UpdateMoveEvent):
                    self.arrival_queue.put((e.time, e))


            print("AFTER")
            self.print_building_state(building)
            self.print_elevator_state(building.elevator, elevator_events[0])

        

