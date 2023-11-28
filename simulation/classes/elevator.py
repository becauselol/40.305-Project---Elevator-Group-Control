from controller import Move


class Elevator:
    def __init__(self, num_floors, capacity=float("inf"), idle_floor=1):
        self.num_floors = num_floors
        self.capacity = capacity
        self.direction = Move.IDLE
        self.floor = idle_floor
        self.move_speed = 2
        self.wait_to_idle = 2
        self.open_door_time = 1

        self.alighting_people = [[] for _ in range(num_floors)]

    def get_num_passengers(self):
        return sum(len(arr) for arr in self.alighting_people)

    def get_alighting(self, floor):
        return self.alighting_people[floor - 1]

    def check_alighting(self, floor):
        return len(self.get_alighting(floor)) > 1

    def clear_alighting(self, floor):
        self.alighting_people[floor - 1] = []
