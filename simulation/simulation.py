from heapq import heappop, heappush, heapify
from numpy.random import exponential

from .classes.building import Building
from .classes import passengerEvents as passE
from .classes import moveEvents as moveE
from .classes.controller import Move
from .classes.DataStore import DataStore


class Simulation:
    def __init__(self, num_floors):
        self.num_floors = num_floors
        self.event_queue = []
        self.cycle_data = DataStore(self.num_floors, 0)

    def initialize_building(self):
        self.building = Building(self.num_floors)
        self.elevator = self.building.elevator
        self.controller = self.building.controller
        

    def initialize_arrivals(self, rate_matrix):
        # check square matrix
        assert len(rate_matrix) == self.num_floors
        for arr in rate_matrix:
            assert len(arr) == self.num_floors

        for i in range(self.num_floors):
            for j in range(self.num_floors):
                if i == j:
                    continue
                rate = rate_matrix[i][j]
                assert rate != 0
                arrival_time = exponential(rate)
                event = passE.ArrivalEvent(
                        arrival_time,
                        i + 1,
                        self.building,
                        j + 1,
                        rate
                    )
                self.event_queue.append((arrival_time, event))

        heapify(self.event_queue)
        
    def reset_cycle_data(self, time):
        self.cycle_data = DataStore(self.num_floors, time)

    def simulate(self, max_time):

        self.initialize_building()

        uniform_rate = 20
        rate_matrix = [[uniform_rate] * self.num_floors for _ in range(self.num_floors)]

        self.initialize_arrivals(rate_matrix)
        # print(self.building.elevator.direction)
        count = 0
        while self.event_queue[0][0] < max_time:

            event_time, event = heappop(self.event_queue)

            # if self.elevator.direction == Move.IDLE:
            # print(event)
            # print(self.elevator.get_num_passengers())
            # print(self.elevator.direction)
            for new_event in event.update():

            # TODO NEED TO REMOVE MoveIdleEvent, if the new Event is a UpdateEvent
                if isinstance(new_event, moveE.UpdateMoveEvent):
                    # remove any existing MoveIdleEvent 
                    new_queue = [(t, e) for t, e in self.event_queue if not isinstance(e, moveE.MoveIdleEvent)]
                    self.event_queue = new_queue
                heappush(self.event_queue, (new_event.time, new_event))


            removed_passengers = event.data_update()
            if removed_passengers:
                self.cycle_data.update_passengers(removed_passengers)

            if isinstance(event, moveE.ReachIdleEvent):
                count += 1
                # yield the cycle data
                self.cycle_data.finalize(event_time)
                yield self.cycle_data

                self.reset_cycle_data(event_time)

        print("NUMBER OF CYCLES")
        print(count)
