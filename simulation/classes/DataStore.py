import pandas as pd

class DataStore:
    def __init__(self, num_floors, start_time):
        self.passenger_dicts = []
        self.start_time = start_time

    def update_passengers(self, passenger_list):
        for passenger in passenger_list:
            passenger.calculate_stats()
            self.passenger_dicts.append(passenger.to_dict())

    def finalize(self, end_time):
        self.passenger_dicts_to_df()
        self.end_time = end_time
        self.cycle_duration = self.end_time - self.start_time

    def passenger_dicts_to_df(self):
        self.passengers = pd.DataFrame(self.passenger_dicts)

    
