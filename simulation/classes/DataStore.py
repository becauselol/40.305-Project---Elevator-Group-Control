import pandas as pd

class DataStore:
    def __init__(self, num_floors):
        self.passenger_dicts = []

    def update_passengers(self, passenger_list):
        for passenger in passenger_list:
            passenger.calculate_stats()
            self.passenger_dicts.append(passenger.to_dict())

    def finalize(self):
        self.passenger_dicts_to_df()

    def passenger_dicts_to_df(self):
        self.passengers = pd.DataFrame(self.passenger_dicts)
