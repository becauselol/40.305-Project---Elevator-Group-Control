from abc import ABC, abstractmethod
import networkx as nx



class ArrivalPattern(ABC):
    def __init__(self, num_floors, total_arrival_rate, arrival_probabilities):
        self.num_floors = num_floors
        self.arrival_probabilities = arrival_probabilities
        self.total_arrival_rate = total_arrival_rate
        self.flow_dict = self.create_flows()

    def create_flows(self):
        G = nx.DiGraph()
        
        for i in range(1, self.num_floors + 1):
            G.add_edge("source", i, capacity=self.arrival_probabilities[i])
        
        for i in range(1, self.num_floors + 1):
            G.add_edge(i, "sink", capacity=self.arrival_probabilities[i])
        
        for i in range(1, self.num_floors + 1):
            for j in range(1, self.num_floors + 1):
                if i == j:
                    continue
                G.add_edge(i, j, capacity=1)
        
        flow_value, flow_dict = nx.maximum_flow(G, "source", "sink")
        assert flow_value == 1, "The probabilities are not maximized"

        return flow_dict

    def get_arrival_rate(i, j):
        assert isinstance(i, int)
        assert isinstance(j, int)
        return 1/(self.flow_dict[i][j] * self.total_arrival_rate)

    def get_rate_matrix():
        rate_matrix = [[0] * num_floors for _ in range(num_floors)]
        for i in range(1, num_floors + 1):
            for j in range(1, num_floors + 1):
                rate_matrix[i-1][j-1] = self.get_arrival_rate(i, j)
        return rate_matrix


class UniformArrival(ArrivalPattern):
    def __init__(self, num_floors, total_arrival_rate):
        super().__init__(num_floors, total_arrival_rate, [1/ num_floors] * num_floors)


class GroundHeavy(ArrivalPattern):
    def __init__(self, num_floors, total_arrival_rate, ground_percentage):
        probabilities = [ground_percentage] + ([(1 - ground_percentage)/(num_floors - 1)] * (num_floors - 1))
        super().__init__(num_floors, total_arrival_rate, probabilities)
