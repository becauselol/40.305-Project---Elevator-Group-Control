from _pytest.compat import num_mock_patch_args
from ..simulation.classes.controller import EqualController, Move

def test_int_call_up():
    num_floors = 4
    controller = EqualController(num_floors)

    controller.add_int_call(3, Move.UP)
    assert Move.UP == controller.where_next_stationary(2, Move.UP)

def test_int_call_down():
    num_floors = 4
    controller = EqualController(num_floors)

    controller.add_int_call(2, Move.DOWN)
    assert Move.DOWN == controller.where_next_stationary(3, Move.DOWN)

def test_ext_board_up():
    num_floors = 4
    controller = EqualController(num_floors)

    controller.add_ext_call(3, Move.UP, 0)
    assert Move.UP == controller.where_next_stationary(2, Move.UP)

    controller = EqualController(num_floors)

    controller.add_ext_call(3, Move.DOWN, 0)
    assert Move.UP == controller.where_next_stationary(2, Move.UP)

def test_ext_board_down():
    num_floors = 4
    controller = EqualController(num_floors)

    controller.add_ext_call(2, Move.UP, 0)
    assert Move.DOWN == controller.where_next_stationary(3, Move.DOWN)

    controller = EqualController(num_floors)

    controller.add_ext_call(2, Move.DOWN, 0)
    assert Move.DOWN == controller.where_next_stationary(3, Move.DOWN)

def test_idle():
    num_floors = 4
    controller = EqualController(num_floors)

    assert Move.WAIT == controller.where_next_stationary(2, Move.DOWN)
    assert Move.WAIT == controller.where_next_stationary(2, Move.UP)
