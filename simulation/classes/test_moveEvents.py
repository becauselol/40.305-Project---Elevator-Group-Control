import moveEvents as move
from building import Building
from controller import Move

class TestNextFloorEvent:
    def test_open_door(self):
        num_floors = 4
        building = Building(num_floors)

        # add some calls
        building.elevator.direction = Move.DOWN
        building.controller.add_int_call(1, Move.DOWN)
        event = move.NextFloorEvent(0, 1, building)
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, move.DoorOpenEvent)
            assert new_event.time == 0
        assert count == 1
        
    def test_next_floor(self):
        num_floors = 4
        building = Building(num_floors)

        # add some calls
        building.elevator.direction = Move.UP
        building.controller.add_ext_call(3, Move.DOWN, 0)

        event = move.NextFloorEvent(0, 2, building)
        new_event = event.update()
        count = 0
        for new_event in event.update():
            count += 1
            assert isinstance(new_event, move.NextFloorEvent)
            assert new_event.time == 0 + building.elevator.move_speed
        assert count == 1


        
        

