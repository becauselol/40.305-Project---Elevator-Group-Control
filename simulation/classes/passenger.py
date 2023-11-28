from controller import Move

class Passenger:
    def __init__(self, spawn_time, source, dest):
        self.spawn_time = spawn_time
        self.source = source
        self.dest = dest

    def get_direction(self):
        return Move.UP if self.dest - self.source > 0 else Move.DOWN
