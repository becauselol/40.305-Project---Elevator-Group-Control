from heapq import heappop, heappush, heapify
from numpy.random import exponential

from classes.building import Building
import classes.passengerEvents as passE
import classes.moveEvents as moveE
# from .DataStore import DataStore


class Simulation:
    def __init__(self):
        self.event_queue = []

    def initialize_building(self):
        self.num_floors = 4
        self.building = Building(self.num_floors)

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
        

    def simulate(self, max_time):

        self.initialize_building()

        rate_matrix = [
                [0, 10, 10, 10],
                [10, 0, 10, 10],
                [10, 10, 0, 10],
                [10, 10, 10, 0]
            ]

        self.initialize_arrivals(rate_matrix)
        print(self.building.elevator.direction)
        while self.event_queue[0][0] < max_time:
            # if
            event_time, event = heappop(self.event_queue)
            print(event)
            for new_event in event.update():
                heappush(self.event_queue, (new_event.time, new_event))
