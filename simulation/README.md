# How to run simulation

Refer to `main.py` for an example

After activating the `venv`, change directory into `simulation` folder and run `py main.py`

## Simple Initialization

```python
simulation = Simulation(num_floors)

for idx, cycle_data in enumerate(simulation.simulate(duration)):
    # DO THINGS WITH CYCLE_DATA
    print("cycle:", idx)
    print("passenger dataframe")
    print(cycle_data.passengers.head())
```
## Cycle Definition

A cycle is defined as between `ReachIdleEvent`.

This event signifies that the elevator has reached its idle state at a specified floor.

Thus a cycle will almost always start with a period of time the elevator is in IDLE for, then it will be triggered by a `ArrivalEvent` and be made to move.

## Endpoints for Analysis

`Simulation.simulate()` is a generator object that will yield `DataStore` objects at the end of each cycle.

### DataStore Object Attributes

#### `start_time`

Float value indicating the start time of the cycle

#### `end_time`

Float value indicating the end time of the cycle

#### `cycle_duration`

Difference between `end_time` and `start_time`

#### `passengers`

`passengers` is a pandas dataframe that has the following attributes for each passenger in the cycle.

|Column|Description|
|---|---|
|`spawn_time`|Time passenger was spawned into the system|
|`source`|Floor that the passenger was spawned on|
|`dest`|Floor that the passenger wants to go to|
|`board_time`|Time passenger boarded the lift|
|`exit_time`|Time passenger left the system|
|`wait_time`|Difference between `board_time` and `spawn_time`|
|`lift_time`|Difference between `exit_time` and `board_time`|
|`sys_time`|Difference between `exit_time` and `spawn_time`|

#### `elevator_state`

`elevator_state` is a pandas dataframe that has the following columns for the elevator's state at any point in time

|Column|Description|
|---|---|
|`elevator_id`|The Id corresponding to the elevator|
|`start_time`|Start time of the state|
|`state`|The state the elevator was in from `start_time` to `end_time`|
|`end_time`|End time of the state|

There are a few state the elevator can be in

|State|Description|
|---|---|
|`Move.IDLE`|Idle State|
|`Move.UP`|Lift is moving UP|
|`Move.DOWN`|Lift is moving DOWN|
|`Move.WAIT`|Lift is waiting but not on the IDLE floor yet|
|`Move.WAIT_UPDATE`|Lift was recently triggered to move, was previously in IDLE/WAIT|
|`Move.MOVE_TO_IDLE`|Lift is currently moving to the idle floor|

### Passengers

# Basically the elevator operating algorithm
## Sequence of events when it reaches the correct floor
CONDITION: elevator is moving in direction up

0. Elevator reaches the floor
    What this means is that we eliminate any internal calls and any external calls

    DOOR OPEN --> triggers ALIGHT if alighting, triggers BOARD 

1. Check if there is anyone alighting

    ALIGHT --> triggers DEPARTURE

2. Alight people
3. wait for a bit
4. check if there is anyone who wants to board in the direction up

    BOARD --> triggers DOOR CLOSE

5. if yes, board them
    update the internal calls

    DOOR CLOSE --> trigger DOOR OPEN if change direction, trigger MOVE TO IDLE if wait, trigger NEXT FLOOR if no change

6. check if we need to change direction
    7. check if there are any people in the lift who still want to go up
    8. check if there are any calls above it that need to respond to
9. if no need to change direction
10. carry on    NEXT FLOOR

11. check if there are any calls below this floor as well (this includes anyone who wants to board on this floor)

    DOOR OPEN --> triggers ALIGHT if alighting, triggers BOARD 

12. if yes, change direction
    This then means we eliminate the external call that is to go down
13. check if there is anyone who wants to board in the direction down

    BOARD --> triggers DOOR CLOSE

14. if yes, board them
    update the internal calls

    DOOR CLOSE --> trigger DOOR OPEN if change direction, trigger MOVE TO IDLE if wait, trigger NEXT FLOOR if no change

14. carry on    NEXT FLOOR

15. If no then just change state to WAIT 

    MOVE TO IDLE

16. And also add event to trigger the movement to Idle


# Things to Update
- Add ArgParser for simulation
- Print cycle data into a .csv file
