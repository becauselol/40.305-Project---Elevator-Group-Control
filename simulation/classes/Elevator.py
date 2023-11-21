class Elevator():

    def __init__(self, capacity, floors, move_speed = 1, start_floor = 1):
        self.capacity = capacity
        self.floors = floors
        self.move_speed = move_speed
        self.current_floor = start_floor

    def move_up(self):
        if self.current_floor + 1 > self.floors:
            raise Exception("Max floor reached")

        self.current_floor += 1

    def move_down(self):
        if self.current_floor - 1 < 1:
            raise Exception("Lowest floor reached")
        
        self.current_floor -= 1

