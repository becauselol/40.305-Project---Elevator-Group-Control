from .controller import Move

class Passenger:
    def __init__(self, spawn_time, source, dest):
        self.spawn_time = spawn_time
        self.source = source
        self.dest = dest

    def get_direction(self):
        return Move.UP if self.dest - self.source > 0 else Move.DOWN

    def set_board_time(self, time):
        self.board_time = time

    def set_exit_time(self, time):
        self.exit_time = time

    def calculate_wait_time(self):
        self.wait_time = self.board_time - self.spawn_time

    def calculate_system_time(self):
        self.sys_time = self.exit_time - self.spawn_time

    def calculate_lift_time(self):
        self.lift_time = self.exit_time - self.board_time

    def calculate_stats(self):
        self.calculate_wait_time()
        self.calculate_lift_time()
        self.calculate_system_time()

    def to_dict(self):
        return {
            "spawn_time": self.spawn_time,
            "source": self.source,
            "dest": self.dest,
            "board_time": self.board_time,
            "exit_time": self.exit_time,
            "wait_time": self.wait_time,
            "sys_time": self.sys_time,
            "lift_time": self.lift_time,
        }

