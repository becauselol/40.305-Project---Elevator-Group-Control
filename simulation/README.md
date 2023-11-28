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

