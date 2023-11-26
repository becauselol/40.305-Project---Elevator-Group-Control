from queue import PriorityQueue
from ..classes.Building import Building
from .DataStore import DataStore


class Simulation:
    
    def __init__(self, num_elevators, num_floors, passenger_arrival_destination_rates):
        self.building = Building(num_elevators, num_floors)
        self.passenger_rates = passenger_arrival_destination_rates
        self.event_queue = PriorityQueue()

        self.data_store = DataStore()
        
    def move_to_idle(self, time, )

    def simulate(self, max_time, building, event_queue: PriorityQueue, data_store):

        update_function = {
            "wait_time": wait_time_update    
        } 
        
        events_simulated = 0
        while (curr_event := event_queue.get()).time < max_time:
            events_simulated += 1
    
            # print time?
    
            update = curr_event.update(**curr_event.params, building=building)
    
            data_update = update["data_store"]
    
            for k, v in data_update.items():
                update_function[k](data_store, v)
    
            new_events = update["new_events"]
    
            for event in new_events:
                event_queue.put(event)
    
        return data_store
    
