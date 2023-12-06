import pandas as pd
import itertools

class DataStore:
    def __init__(self, num_floors, start_time, num_elevators, state):
        self.passenger_dicts = []
        self.num_elevators = num_elevators
        self.elevator_state_dicts = {i: [
                {
                    "elevator_id": i,
                    "start_time": start_time,
                    "state": state
                }
            ] for i in range(1, num_elevators + 1)}
        self.start_time = start_time

    def update_passengers(self, passenger_list):
        for passenger in passenger_list:
            passenger.calculate_stats()
            self.passenger_dicts.append(passenger.to_dict())

    def finalize(self, end_time):
        self.passenger_dicts_to_df()

        for i in self.elevator_state_dicts:
            self.elevator_state_dicts[i][-1]["end_time"] = end_time

        self._massive_arr = []
        for i in self.elevator_state_dicts.values():
            self._massive_arr += i
        self.elevator_state = pd.DataFrame(self._massive_arr)

        self.end_time = end_time
        self.cycle_duration = self.end_time - self.start_time

    def passenger_dicts_to_df(self):
        self.passengers = pd.DataFrame(self.passenger_dicts)

    def update_elevator_state(self, time, elevator_id, state):
        new_state_data = {
                "elevator_id": elevator_id,
                "start_time": time,
                "state": state
            }
        if self.elevator_state_dicts:
            self.elevator_state_dicts[elevator_id][-1]["end_time"] = time

        self.elevator_state_dicts[elevator_id].append(new_state_data)

