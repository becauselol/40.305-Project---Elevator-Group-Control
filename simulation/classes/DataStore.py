import pandas as pd

class DataStore:
    def __init__(self, num_floors, start_time, state):
        self.passenger_dicts = []
        self.elevator_state_dicts = [
                {
                    "start_time": start_time,
                    "state": state
                }
            ]
        self.start_time = start_time

    def update_passengers(self, passenger_list):
        for passenger in passenger_list:
            passenger.calculate_stats()
            self.passenger_dicts.append(passenger.to_dict())

    def finalize(self, end_time):
        self.passenger_dicts_to_df()

        self.elevator_state_dicts[-1]["end_time"] = end_time
        self.elevator_state = pd.DataFrame(self.elevator_state_dicts)

        self.end_time = end_time
        self.cycle_duration = self.end_time - self.start_time

    def passenger_dicts_to_df(self):
        self.passengers = pd.DataFrame(self.passenger_dicts)

    def update_elevator_state(self, time, state):
        new_state_data = {
                "start_time": time,
                "state": state
            }
        if self.elevator_state_dicts:
            self.elevator_state_dicts[-1]["end_time"] = time

        self.elevator_state_dicts.append(new_state_data)

