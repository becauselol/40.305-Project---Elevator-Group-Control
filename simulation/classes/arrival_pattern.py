import math
from abc import ABC, abstractmethod
import networkx as nx



class ArrivalPattern(ABC):
    def __init__(self, num_floors, total_arrival_rate, arrival_probabilities):
        self.num_floors = num_floors
        self.arrival_probabilities = arrival_probabilities
        self.total_arrival_rate = total_arrival_rate

        # self.flow_dict = self.create_flows()

    # scrapped idea
    def create_flows(self):
        G = nx.DiGraph()
        
        for i in range(1, self.num_floors + 1):
            G.add_edge("source", f"{i}_from", capacity=self.arrival_probabilities[i - 1])
        
        for i in range(1, self.num_floors + 1):
            G.add_edge(f"{i}_to", "sink", capacity=self.arrival_probabilities[i - 1])
        
        for i in range(1, self.num_floors + 1):

            for j in range(1, self.num_floors + 1):
                if i == j:
                    continue
                G.add_edge(f"{i}_from", f"{j}_to", capacity=1)
        
        flow_value, flow_dict = nx.maximum_flow(G, "source", "sink")
        for k, v in flow_dict.items():
            for sub_k, f in v.items():
                print(type(k))
                print(k, sub_k, f)
        print(flow_value)
        assert math.isclose(flow_value, 1), "The probabilities are not maximized"

        return flow_dict

    def get_arrival_rate(self, i, j):
        assert isinstance(i, int)
        assert isinstance(j, int)
        return 1/(self.flow_dict[f"{i}_from"][f"{j}_to"] * self.total_arrival_rate)

    def get_rate_matrix(self):
        rate_matrix = [[0] * self.num_floors for _ in range(self.num_floors)]
        for i in range(1, self.num_floors + 1):
            for j in range(1, self.num_floors + 1):
                if i == j:
                    continue
                rate_matrix[i-1][j-1] = self.get_arrival_rate(i, j)
        return rate_matrix


class UniformArrival(ArrivalPattern):
    def __init__(self, num_floors, total_arrival_rate):
        super().__init__(num_floors, total_arrival_rate, [1/ num_floors] * num_floors)

    def get_arrival_rate(self, i, j):
        assert isinstance(i, int)
        assert isinstance(j, int)
        return 1/ (self.total_arrival_rate / ((self.num_floors**2) - self.num_floors))



class GroundHeavy(ArrivalPattern):
    def __init__(self, num_floors, total_arrival_rate, ground_percentage):
        self.ground_percentage = ground_percentage
        self.num_floors = num_floors
        self.total_arrival_rate = total_arrival_rate
        self.probability_matrix = self.get_prob_matrix()

    def get_prob_matrix(self):
        prob_matrix = [[0] * self.num_floors for _ in range(self.num_floors)]
        other_percentage = (1 - self.ground_percentage)/(self.num_floors - 1)
        ground_rate = (self.ground_percentage / (self.num_floors - 1))

        assert ground_rate < other_percentage, "too many people going up"
        residual_percentage = (other_percentage - ground_rate) / (self.num_floors - 2)

        for j in range(1, len(prob_matrix[0])):
            prob_matrix[0][j] = ground_rate
            prob_matrix[j][0] = ground_rate

        for i in range(1, len(prob_matrix)):
            for j in range(1, len(prob_matrix[i])):
                if i == j:
                    continue
                prob_matrix[i][j] = residual_percentage

        return prob_matrix

    def get_arrival_rate(self, i, j):
        return 1/ (self.total_arrival_rate * self.probability_matrix[i-1][j-1])



