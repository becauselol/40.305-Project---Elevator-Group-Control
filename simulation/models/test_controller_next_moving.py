import pytest
from controller import EqualController, Move

def test_controller_get_closest_up():
    num_floors = 4 
    controller = EqualController(num_floors)

    controller.add_ext_call(4, Move.UP , 0)
    assert 4 == controller.where_next_moving(2, Move.UP)

    controller.add_int_call(3, Move.UP)
    assert 3 == controller.where_next_moving(2, Move.UP)
    assert 3 == controller.where_next_moving(3, Move.UP)

def test_controller_get_farthest_down():
    num_floors = 4 
    controller = EqualController(num_floors)

    controller.add_ext_call(4, Move.DOWN, 0)
    assert 4 == controller.where_next_moving(2, Move.UP)

    controller.add_ext_call(3, Move.DOWN, 0)
    assert 4 == controller.where_next_moving(2, Move.UP)
    assert 4 == controller.where_next_moving(3, Move.UP)

def test_controller_get_closest_down():
    num_floors = 4 
    controller = EqualController(num_floors)

    controller.add_ext_call(2, Move.DOWN, 0)
    assert 2 == controller.where_next_moving(4, Move.DOWN)

    controller.add_int_call(1, Move.DOWN)
    assert 2 == controller.where_next_moving(2, Move.DOWN)

    
def test_controller_get_furthest_up():
    num_floors = 4 
    controller = EqualController(num_floors)

    controller.add_ext_call(2, Move.UP, 0)
    assert 2 == controller.where_next_moving(4, Move.DOWN)
    controller.add_ext_call(3, Move.UP ,0)
    assert 2 == controller.where_next_moving(4, Move.DOWN)

def test_controller_should_throw_error():
    num_floors = 4 
    controller = EqualController(num_floors)

    controller.add_ext_call(2, Move.DOWN, 0)
    with pytest.raises(Exception) as excinfo:
        controller.where_next_moving(4, Move.UP)

    assert str(excinfo.value) == "No remaining calls in selected direction"

