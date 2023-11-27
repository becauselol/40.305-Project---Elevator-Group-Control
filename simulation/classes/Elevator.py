from heapq import heappush, heappop
from enum import Enum


class Move(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0



class Elevator:

    def __init__(self, capacity, floors, move_speed = 1, start_floor = 1):
        self.capacity = capacity
        self.floors = floors
        self.move_speed = move_speed
        self.current_floor = start_floor
        self.direction = Move.IDLE
        self.wait_time = 0.5
        self.wait_idle_time = 2

        self.alighting_people = [[] for _ in range(floors)]

    def move_up(self):
        if self.current_floor + 1 > self.floors:
            raise Exception("Max floor reached")

        self.current_floor += 1

    def move_down(self):
        if self.current_floor - 1 < 1:
            raise Exception("Lowest floor reached")
        
        self.current_floor -= 1

    def move_down_n(self, n):
        for _ in range(n):
            self.move_down()

    def move_up_n(self, n):
        for _ in range(n):
            self.move_up()

    def get_num_passengers(self):
        return sum([len(arr) for arr in self.alighting_people])

    def add_passenger(self, passenger):
        self.alighting_people[passenger.dest - 1].append(passenger)

class ExtCall:
    def __init__(self, floor):
        self.floor = floor
        self.up_call = False
        self.down_call = False
        self.up_call_time = float("inf")
        self.down_call_time = float("inf")

    def set_up_call(self, time):
        if self.up_call:
            return
        
        self.up_call = True
        self.up_call_time = time

    def set_down_call(self, time):
        if self.down_call:
            return
        
        self.down_call = True
        self.down_call_time = time

    def no_call(self):
        return not self.up_call and not self.down_call

    def min_call(self):
        if self.up_call_time < self.down_call_time:
            return self.up_call_time 
        else:
            return self.down_call_time


class ElevatorController:

    def __init__(self, num_floors):
        # Maintain 3 things
        # Number to pick up
        # Up pq, Dwon pq
        # Then just subtract the number to pick up as you go along
        # up calls
        self.idle_floor = 1

        self.ext_call = [ExtCall(i) for i in range(1, num_floors + 1)]

        # These are the internal calls
        self.int_call = []


    def add_ext_call(self, time, elevator, floor_call, direction):
        if direction == Move.UP:
            self.ext_call[floor_call - 1].set_up_call(time)
        elif direction == Move.DOWN:
            self.ext_call[floor_call - 1].set_down_call(time)


    def add_int_call(self, time, elevator, floor_call):
        if floor_call * elevator.direction.value not in self.int_call:
            heappush(self.int_call, floor_call * elevator.direction.value)

    def request_is_empty(self):
        return len(self.int_call) == 0 and all([e_call.no_call() for e_call in self.ext_call])

    def consume_ext_call(self, floor, move_direction):
        if move_direction == Move.UP:
            self.ext_call[floor - 1].up_call = False
            self.ext_call[floor - 1].up_call_time = float("inf")
        elif move_direction == Move.DOWN:
            self.ext_call[floor - 1].down_call = False
            self.ext_call[floor - 1].down_call_time = float("inf")

    def update_ext_call_priority(self, floor, move_direction, new_call_time):
        if move_direction == Move.UP:
            self.ext_call[floor - 1].up_call_time = new_call_time
        elif move_direction == Move.DOWN:
            self.ext_call[floor - 1].down_call_time = new_call_time

    def consume_int_call(self, floor, move_direction):
        print("call to consume:", floor * move_direction.value)
        if floor * move_direction.value in self.int_call:
            self.int_call = [v for v in self.int_call if v != floor * move_direction.value]



    def check_next_move(self, time, elevator, moving=False, current_move_floor=-1):
        """
        Return the parameters of the next move that the elevator is supposed to do
        """
        # Check if the queues are empty
        if self.request_is_empty():
            return -1

        # If elevator is idle, figure out which direction to move
        if elevator.direction == Move.IDLE:
            # Check what is the minimum direction
            min_times = [e_call.min_call() for e_call in self.ext_call]
            min_time = min(min_times)

            target_floor = min_times.index(min_time) + 1
            
            elevator.direction = Move.UP if elevator.current_floor < target_floor else Move.DOWN
            print("updated direction:", elevator.direction)
            

        # If elevator is moving along a certain direction, check what the next move is supposed to be
        # If elevator is on up progress
        print("ext_down_calls:", [e_call.down_call for e_call in self.ext_call])
        print("ext_up_calls:", [e_call.up_call for e_call in self.ext_call])
        print("int_calls:", self.int_call)
        if elevator.direction == Move.UP:
            print("CONSIDERING MOVING UP")
            min_floor = float("inf")
            if self.int_call:
                min_floor = min(min_floor, self.int_call[0])

            # Should only check floors above current_floor
            for index in range(elevator.current_floor, len(self.ext_call)):
                e_call = self.ext_call[index]
                if e_call.up_call:
                    min_floor = min(min_floor, e_call.floor)
                    break

            if min_floor != float("inf"):
                # We have found the next floor to go to
                return min_floor
                # Time to change direction

            # Check if there are any down calls to respond to
            # does not checks the current floor as well
            for index in range(len(self.ext_call) -1, elevator.current_floor - 1, -1):
                e_call = self.ext_call[index]
                if e_call.down_call:
                    print(e_call.floor)
                    return e_call.floor

            # lastly, if there is a call on the current floor
            # We need to let them board first
            if self.ext_call[elevator.current_floor - 1].up_call:
                return elevator.current_floor
            
            # Idea is we can't interrupt the progress
            if moving:
                return current_move_floor

            elevator.direction = Move.DOWN
            print("DECIDED TO MOVE DOWN")
            # Now the max_floor is the next_floor to go to
            for index in range(elevator.current_floor - 2, -1, -1):
                e_call = self.ext_call[index]
                if e_call.down_call:
                    return e_call.floor

        elif elevator.direction == Move.DOWN:
            print("CONSIDERING MOVING DOWN")
            max_floor = float("-inf")
            if self.int_call:
                max_floor = max(max_floor, -1 * self.int_call[0])

            # Should not check current floor
            for index in range(elevator.current_floor - 2, -1, -1):
                e_call = self.ext_call[index]
                if e_call.down_call:
                    max_floor = max(max_floor, e_call.floor)
                    break

            if max_floor != float("-inf"):
                return max_floor

            # check if there are any up calls to respond to
            # Should not check current floor
            for index in range(0, elevator.current_floor - 1):
                e_call = self.ext_call[index]
                if e_call.up_call:
                    return e_call.floor

            if self.ext_call[elevator.current_floor - 1].down_call:
                return elevator.current_floor

            # Idea is we can't interrupt the progress
            if moving:
                return current_move_floor

            elevator.direction = Move.UP
            print("DECIDED TO MOVE UP")
            
            # Now we need to consider the up call, cannot include current floor
            for index in range(elevator.current_floor, len(self.ext_call)):
                e_call = self.ext_call[index]
                if e_call.up_call:
                    return e_call.floor

        print("somehow didnt get any scenarios")
        return -1


    def get_new_call(self, time, elevator, event):
        """
        Check what the new call is and respond accordingly
        """
        pass

    def interrupt_move(self, time, elevator, reachFloorEvent):
        """
        Figure out what is the update required to the reachFloorEvent
        and return the updated reachFloorEvent parameters
        """
        pass

    def get_idle_floor(self, elevator):
        """
        Eventually controller will access elevators to determine
        Which IDLE direction
        """
        return self.idle_floor

    def move_idle_direction(self, elevator):
        return Move.UP.value if elevator.current_floor < self.idle_floor else Move.DOWN.value

