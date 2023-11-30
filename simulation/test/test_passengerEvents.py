from simulation.classes import moveEvents as moveE
from simulation.classes import passengerEvents as passE
from simulation.classes.building import Building
from simulation.classes.controller import Move
from simulation.classes.passenger import Passenger

class TestArrival:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def test_update_move(self):
        event = passE.ArrivalEvent(0, 2, self.building, 3, 1)
        count = 0
        for new_event in event.update():
            count += 1
            if count == 1:
                assert isinstance(new_event, passE.ArrivalEvent)
            elif count == 2:
                assert isinstance(new_event, moveE.UpdateMoveEvent)

        assert count == 2
        
        # check that passenger is added
        assert len(self.building.get_boarding(2, Move.UP)) == 1

        # check that the call is added
        assert self.controller.ext_call[2 - 1].up_call
        assert self.controller.ext_call[2 - 1].up_call_time == 0
        assert self.elevator.direction == Move.WAIT_UPDATE

    def test_no_update(self):
        self.elevator.direction = Move.UP
        event = passE.ArrivalEvent(0, 2, self.building, 3, 1)
        count = 0
        for new_event in event.update():
            count += 1
            if count == 1:
                assert isinstance(new_event, passE.ArrivalEvent)

        assert count == 1
        
        # check that passenger is added
        assert len(self.building.get_boarding(2, Move.UP)) == 1
        # check that the call is added
        assert self.controller.ext_call[2 - 1].up_call
        assert self.controller.ext_call[2 - 1].up_call_time == 0

    def test_no_update_move_idle(self):
        self.elevator.direction = Move.MOVE_TO_IDLE
        event = passE.ArrivalEvent(0, 2, self.building, 3, 1)
        count = 0
        for new_event in event.update():
            count += 1
            if count == 1:
                assert isinstance(new_event, passE.ArrivalEvent)

        assert count == 1
        
        # check that passenger is added
        assert len(self.building.get_boarding(2, Move.UP)) == 1

        # check that the call is added
        assert self.controller.ext_call[2 - 1].up_call
        assert self.controller.ext_call[2 - 1].up_call_time == 0


class TestAlight:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def test_to_departure(self):
        self.elevator.floor = 2
        passenger = Passenger(0, 1, 2)
        self.elevator.add_passenger(passenger)
        event = passE.AlightEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, passE.DepartureEvent)

        assert count == 1
        assert self.elevator.get_num_passengers() == 0
        assert len(self.building.alighted_people[2 - 1]) == 1

class TestDeparture:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        self.elevator = self.building.elevator
        self.controller = self.building.controller

    def test_to_door_close(self):
        passenger = Passenger(0, 1, 2)
        self.elevator.add_passenger(passenger)
        self.building.remove_passenger_from_elevator(2)
        event = passE.DepartureEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.DoorCloseEvent)

        assert count == 1
        assert len(self.building.alighted_people[2 - 1]) == 0

class TestBoard:
    def setup_method(self, method):
        num_floors = 4
        self.building = Building(num_floors)

        self.elevator = self.building.elevator
        self.controller = self.building.controller

        self.elevator.floor = 2
        self.elevator.direction = Move.UP

    def test_to_next_floor(self):
        passenger = Passenger(0, 2, 3)
        self.building.add_passenger_to_floor(2, passenger)

        event = passE.BoardEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.NextFloorEvent)

        assert count == 1
        assert self.controller.int_call == [3]

    def test_to_next_floor_full(self):
        self.elevator.capacity = 1
        for i in range(2):
            passenger = Passenger(i, 2, 3)
            self.building.add_passenger_to_floor(2, passenger)

        event = passE.BoardEvent(0, 2, self.building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, moveE.NextFloorEvent)

        assert count == 1
        assert self.controller.int_call == [3]
        assert self.controller.ext_call[2 - 1].up_call
        assert self.controller.ext_call[2 - 1].up_call_time == 1


