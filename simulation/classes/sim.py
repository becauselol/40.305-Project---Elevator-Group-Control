from heapq import heappop, heappush, heapify
from numpy.random import exponential

from simulation.classes import elevator

from .building import Building
from . import passengerEvents as passE
from . import moveEvents as moveE
from .controller import Move
from .DataStore import DataStore


class Simulation:
    def __init__(self, num_floors):
        self.num_floors = num_floors
        self.event_queue = []

    def initialize_building(self):
        self.num_elevators = 2
        self.building = Building(self.num_floors, self.num_elevators)
        self.elevators = self.building.elevators
        self.controller = self.building.groupController

        self.cycle_data = DataStore(self.num_floors, 0, self.num_elevators, self.elevators[1].direction)
        

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
        
    def reset_cycle_data(self, time, elevator_state):
        self.cycle_data = DataStore(self.num_floors, time, self.num_elevators, elevator_state)

    def reset_simulation(self):
        self.event_queue = []

    def simulate(self, max_time):
        self.reset_simulation()

        self.initialize_building()
        self.reset_cycle_data(0, self.elevators[1].direction)

        uniform_rate = 20
        rate_matrix = [[uniform_rate] * self.num_floors for _ in range(self.num_floors)]

        self.initialize_arrivals(rate_matrix)
        # print(self.building.elevator.direction)
        count = 0
        while self.event_queue[0][0] < max_time:

            event_time, event = heappop(self.event_queue)

            # if self.elevators[1].direction == Move.IDLE:
            # print(event)
            # print(self.elevators[1].get_num_passengers())
            # print(self.elevators[1].direction)

            previous_elevator_state = {i: self.elevators[i].direction for i in self.elevators.keys()}

            # RUN the updates and create any new events as required
            for new_event in event.update():

            # NEED TO REMOVE MoveIdleEvent, if the new Event is a UpdateEvent
                if isinstance(new_event, moveE.UpdateMoveEvent):
                    # remove any existing MoveIdleEvent 
                    # remove the corresponding MoveIdleEvent
                    new_queue = [(t, e) for t, e in self.event_queue if not (isinstance(e, moveE.MoveIdleEvent) and e.elevator_id == new_event.elevator_id)]
                    self.event_queue = new_queue

                heappush(self.event_queue, (new_event.time, new_event))

            new_elevator_state = {i: self.elevators[i].direction for i in self.elevators.keys()}

            for i in self.elevators.keys():
                if previous_elevator_state[i] != new_elevator_state[i]:
                    self.cycle_data.update_elevator_state(event_time, i, new_elevator_state)

            removed_passengers = event.data_update()
            if removed_passengers:
                self.cycle_data.update_passengers(removed_passengers)

            if isinstance(event, moveE.ReachIdleEvent):
                count += 1
                # yield the cycle data
                self.cycle_data.finalize(event_time)
                yield self.cycle_data

                self.reset_cycle_data(event_time, self.elevators[1].direction)
