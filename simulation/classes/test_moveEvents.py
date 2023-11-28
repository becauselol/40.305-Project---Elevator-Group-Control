import moveEvents as moveE
import passengerEvents as passE
from building import Building
from controller import Move
from passenger import Passenger

class TestNextFloorEvent:
    def test_open_door(self):
        num_floors = 4
        building = Building(num_floors)

        # add some calls
        building.elevator.direction = Move.DOWN
        building.controller.add_int_call(1, Move.DOWN)
        event = moveE.NextFloorEvent(0, 1, building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.DoorOpenEvent)
            assert new_event.time == 0
        assert count == 1
        
    def test_next_floor(self):
        num_floors = 4
        building = Building(num_floors)

        # add some calls
        building.elevator.direction = Move.UP
        building.controller.add_ext_call(3, Move.DOWN, 0)

        event = moveE.NextFloorEvent(0, 2, building)
        new_event = event.update()
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.NextFloorEvent)
            assert new_event.time == 0 + building.elevator.move_speed
        assert count == 1


        
class TestDoorOpen:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        # add some calls
        self.building.elevator.direction = Move.UP
        self.building.elevator.floor = 2

    def test_door_close_event(self):
        self.building.controller.add_ext_call(2, Move.UP, 0)

        event = moveE.DoorOpenEvent(0, 2, self.building)
        
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.DoorCloseEvent)
            assert new_event.time == event.time + self.building.elevator.open_door_time

        assert self.building.controller.request_is_empty() == True

        assert count == 1

    def test_alight_event(self):
        passenger = Passenger(0, 1, 2)
        self.building.add_passenger_to_floor(1, passenger)
        self.building.add_passenger_to_elevator(1, Move.UP)
        self.building.controller.add_int_call(2, Move.UP)

        event = moveE.DoorOpenEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, passE.AlightEvent)
            assert new_event.time == event.time 

        assert self.building.controller.request_is_empty() == True

        assert count == 1

        
class TestDoorClose:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        # add some calls
        self.building.elevator.direction = Move.UP
        self.building.elevator.floor = 2
        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def teardown_method(self, method):
        self.elevator.direction = Move.UP

    def test_next_floor(self):
        self.controller.add_ext_call(3, Move.DOWN, 0)
        event = moveE.DoorCloseEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.NextFloorEvent)
            assert new_event.time == event.time + self.elevator.move_speed
        assert count == 1
        assert self.building.elevator.direction == Move.UP


    def test_board(self):
        assert self.elevator.direction == Move.UP
        passenger = Passenger(0, 2, 3)
        self.building.add_passenger_to_floor(2, passenger)

        assert self.building.check_boarding(2, Move.UP)

        event = moveE.DoorCloseEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, passE.BoardEvent)
            assert new_event.time == event.time
        assert count == 1
        assert self.building.elevator.direction == Move.UP


    def test_move_idle(self):
        event = moveE.DoorCloseEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.MoveIdleEvent)
            assert new_event.time == event.time + self.building.elevator.wait_to_idle
        assert count == 1
        assert self.building.elevator.direction == Move.WAIT


    def test_stay_idle(self):
        self.elevator.floor = 1
        event = moveE.DoorCloseEvent(0, 1, self.building)
        count = 0
        for new_event in event.update():
            count += 1
        assert count == 0
        assert self.building.elevator.direction == Move.IDLE


class TestMoveIdle:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        # add some calls
        self.building.elevator.direction = Move.WAIT
        self.building.elevator.floor = 2
        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def test_move_idle(self):
        event = moveE.MoveIdleEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.ReachIdleEvent)

        assert count == 1
        assert self.elevator.direction == Move.MOVE_TO_IDLE


class TestReachIdle:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        # add some calls
        self.building.elevator.direction = Move.MOVE_TO_IDLE
        self.building.elevator.floor = 3
        self.elevator = self.building.elevator
        self.controller = self.building.controller


    def test_reach_stay_idle(self):
        assert self.controller.request_is_empty()

        event = moveE.ReachIdleEvent(0, self.controller.get_idle_floor(self.elevator), self.building)
        count = 0
        for new_event in event.update():
            count += 1
        assert count == 0
        assert self.elevator.floor == self.controller.get_idle_floor(self.elevator)
        assert self.elevator.direction == Move.IDLE


    def test_reach_update_move(self):
        self.controller.add_ext_call(3, Move.UP, 0)

        assert not self.controller.request_is_empty()
        event = moveE.ReachIdleEvent(0, self.controller.get_idle_floor(self.elevator), self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.UpdateMoveEvent)
            assert new_event.time == event.time

        assert count == 1
        assert self.elevator.floor == self.controller.get_idle_floor(self.elevator)
        assert self.elevator.direction == Move.IDLE


class TestUpdateMove:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        # add some calls
        self.building.elevator.direction = Move.WAIT
        self.building.elevator.floor = 2
        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def test_up_call_ext(self):
        self.controller.add_ext_call(2, Move.UP, 0)

        event = moveE.UpdateMoveEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.NextFloorEvent)
            assert event.time == new_event.time

        assert count == 1
        assert self.elevator.direction == Move.UP




